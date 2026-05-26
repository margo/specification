from __future__ import annotations

import logging

from .resolver import collect_attributes, resolve_range, resolve_union_expr
from .types import (
    ARRAY_CONSTRAINT_MAP,
    NUMERIC_CONSTRAINT_MAP,
    STRING_CONSTRAINT_MAP,
    COMPOSITION_MAP,
)

logger = logging.getLogger(__name__)


def _apply_scalar_constraints(prop_schema: dict, attr_def: dict) -> dict:
    """
    Apply pattern, min/max length, and numeric range constraints
    to a scalar property schema in-place.

    Handles:
      pattern              → pattern
      min_length           → minLength
      max_length           → maxLength
      minimum_value        → minimum
      maximum_value        → maximum
      exclusive_minimum_value → exclusiveMinimum
      exclusive_maximum_value → exclusiveMaximum
    """
    schema_type = prop_schema.get("type")

    # String constraints
    if schema_type == "string":
        for linkml_key, openapi_key in STRING_CONSTRAINT_MAP.items():
            if linkml_key in attr_def:
                prop_schema[openapi_key] = attr_def[linkml_key]

    # Numeric constraints
    if schema_type in ("integer", "number"):
        for linkml_key, openapi_key in NUMERIC_CONSTRAINT_MAP.items():
            if linkml_key in attr_def:
                prop_schema[openapi_key] = attr_def[linkml_key]

    return prop_schema


def _apply_array_constraints(prop_schema: dict, attr_def: dict) -> dict:
    """
    Apply cardinality constraints to an array property schema in-place.

    Handles:
      minimum_cardinality  → minItems
      maximum_cardinality  → maxItems
      exact_cardinality    → minItems + maxItems (same value)
    """
    # exact_cardinality takes precedence
    if "exact_cardinality" in attr_def:
        exact = attr_def["exact_cardinality"]
        prop_schema["minItems"] = exact
        prop_schema["maxItems"] = exact
        return prop_schema

    for linkml_key, openapi_key in ARRAY_CONSTRAINT_MAP.items():
        if openapi_key and linkml_key in attr_def:
            prop_schema[openapi_key] = attr_def[linkml_key]

    return prop_schema


def _build_range_schema(
    resolved: dict,
    attr_def: dict,
    schema: dict,
    visited: set[str],
) -> dict:
    """
    Build the core OpenAPI schema fragment for a resolved range.
    Does NOT apply description, example, or array wrapping —
    those are handled by the caller.
    """
    if resolved["kind"] == "enum":
        return {"$ref": f"#/components/schemas/{resolved['name']}"}

    if resolved["kind"] == "class":
        nested_name = resolved["name"]
        if attr_def.get("inlined"):
            return convert_class(nested_name, schema, inline=True, _visited=visited)
        return {"$ref": f"#/components/schemas/{nested_name}"}

    # Scalar
    return dict(resolved["schema"])


def _resolve_composition(
    attr_def: dict,
    schema: dict,
) -> dict | None:
    """
    Check whether an attribute carries any LinkML composition keywords
    (any_of, all_of, exactly_one_of, none_of) and resolve them into
    an OpenAPI composition fragment.

    If multiple composition keywords are present they are merged under allOf.

    Returns None if no composition keywords are found.

    LinkML examples:

      # anyOf — value is string OR integer
      myAttr:
        any_of:
          - range: string
          - range: integer

      # allOf — value must satisfy ALL constraints
      myAttr:
        range: MyBase
        all_of:
          - range: MyMixin

      # Combining range + any_of (range acts as allOf base)
      myAttr:
        range: string
        any_of:
          - pattern: "^foo.*"
          - pattern: "^bar.*"
    """
    fragments: list[dict] = []

    for linkml_key, openapi_key in COMPOSITION_MAP.items():
        if linkml_key not in attr_def:
            continue
        fragment = resolve_union_expr(attr_def[linkml_key], schema, openapi_key)
        fragments.append(fragment)

    if not fragments:
        return None

    if len(fragments) == 1:
        return fragments[0]

    # Multiple composition keywords — wrap in allOf
    return {"allOf": fragments}


def _build_is_a_allof(class_name: str, schema: dict) -> list[dict] | None:
    """
    If a class has is_a, emit an allOf reference to the parent so that
    OpenAPI consumers understand the inheritance relationship explicitly,
    in addition to the attribute merging done by collect_attributes.

    This is optional but makes the inheritance visible in generated docs.
    """
    class_def = schema["classes"].get(class_name, {})
    parent = class_def.get("is_a")
    if not parent:
        return None
    return [{"$ref": f"#/components/schemas/{parent}"}]


def convert_enum(enum_name: str, schema: dict) -> dict:
    """
    Convert a LinkML enum definition to an OpenAPI schema.

    LinkML:
      DeviceRole:
        permissible_values:
          Standalone Cluster:
          Standalone Device:

    OpenAPI:
      type: string
      enum: [Standalone Cluster, Standalone Device]
    """
    enum_def = schema["enums"][enum_name]
    values = list((enum_def.get("permissible_values") or {}).keys())

    result: dict = {"type": "string", "enum": values}

    if enum_def.get("description"):
        result["description"] = enum_def["description"]

    return result


def convert_class(
    class_name: str,
    schema: dict,
    *,
    inline: bool = False,
    emit_allof_inheritance: bool = True,
    _visited: set[str] | None = None,
) -> dict:
    """
    Convert a LinkML class to an OpenAPI schema object.

    Handles:
      - Scalar attributes                → simple type
      - equals_string                    → type: string, enum: [value]
      - Nested class (range)             → $ref or inlined object
      - Enum range                       → $ref to enum schema
      - multivalued                      → type: array, items: ...
      - inlined: true                    → recursively expand nested class
      - required: true                   → added to required[]
      - is_a / mixins inheritance        → attributes merged + allOf $ref
      - pattern / min_length / max_length
      - minimum_value / maximum_value / exclusive bounds
      - minimum_cardinality / maximum_cardinality / exact_cardinality
      - any_of                           → anyOf
      - all_of                           → allOf
      - exactly_one_of                   → oneOf
      - none_of                          → not
      - range + any_of combined          → allOf: [$ref, anyOf: [...]]
    """
    _visited = _visited or set()
    if class_name in _visited:
        logger.warning("Circular reference detected for class '%s'", class_name)
        return {"$ref": f"#/components/schemas/{class_name}"}
    _visited = _visited | {class_name}

    class_def = schema["classes"].get(class_name, {})
    attributes = collect_attributes(class_name, schema)

    properties: dict = {}
    required: list[str] = []

    for attr_name, attr_def in attributes.items():
        prop_schema: dict = {}
        resolved = resolve_range(attr_def.get("range"), schema)
        is_multivalued = bool(attr_def.get("multivalued"))

        # ── Check for composition keywords on this attribute ──────────────────
        composition = _resolve_composition(attr_def, schema)

        # ── equals_string → single-value enum ────────────────────────────────
        if "equals_string" in attr_def:
            prop_schema = {
                "type": "string",
                "enum": [attr_def["equals_string"]],
            }
            # pattern still valid on a fixed enum — skip numeric constraints
            _apply_scalar_constraints(prop_schema, attr_def)
        
        # ── Composition only (no plain range) ─────────────────────────────────
        elif composition and not attr_def.get("range"):
            prop_schema = composition

        # ── Range + composition (e.g. range: string + any_of: [...patterns]) ──
        elif composition and attr_def.get("range"):
            base = _build_range_schema(resolved, attr_def, schema, _visited)
            _apply_scalar_constraints(base, attr_def)
            # Combine: the range is the base type, composition adds constraints
            prop_schema = {"allOf": [base, composition]}

        # ── Enum range ────────────────────────────────────────────────────────
        elif resolved["kind"] == "enum":
            ref = {"$ref": f"#/components/schemas/{resolved['name']}"}
            if is_multivalued:
                prop_schema = {"type": "array", "items": ref}
                _apply_array_constraints(prop_schema, attr_def)
            else:
                prop_schema = ref

        # ── Nested class ──────────────────────────────────────────────────────
        elif resolved["kind"] == "class":
            nested_name = resolved["name"]

            nested = _build_range_schema(resolved, attr_def, schema, _visited)

            # if attr_def.get("inlined"):
            #     nested = convert_class(
            #         nested_name, schema, inline=True, _visited=_visited
            #     )
            # else:
            #     nested = {"$ref": f"#/components/schemas/{nested_name}"}

            if is_multivalued:
                prop_schema = {"type": "array", "items": nested}
                _apply_array_constraints(prop_schema, attr_def)
            else:
                prop_schema = nested

        # ── Scalar ────────────────────────────────────────────────────────────
        else:
            base = dict(resolved["schema"])
            _apply_scalar_constraints(base, attr_def)

            if is_multivalued:
                prop_schema = {"type": "array", "items": base}
                _apply_array_constraints(prop_schema, attr_def)
            else:
                prop_schema = base

        # Attach description
        if attr_def.get("description"):
            prop_schema["description"] = attr_def["description"]

        # Attach example
        if "example" in attr_def:
            prop_schema["example"] = attr_def["example"]

        properties[attr_name] = prop_schema

        if attr_def.get("required"):
            required.append(attr_name)

    # ── Build the class-level object schema ───────────────────────────────────
    object_schema: dict = {
        "type": "object",
        "properties": properties,
    }

    if class_def.get("description"):
        object_schema["description"] = class_def["description"]

    if required:
        object_schema["required"] = required

    # ── Class-level composition (any_of / all_of on the class itself) ─────────
    class_composition = _resolve_composition(class_def, schema)

    # ── is_a inheritance → allOf $ref ─────────────────────────────────────────
    allof_parents = (
        _build_is_a_allof(class_name, schema)
        if emit_allof_inheritance
        else None
    )

    if allof_parents or class_composition:
        allof_members: list[dict] = []

        if allof_parents:
            allof_members.extend(allof_parents)

        allof_members.append(object_schema)

        if class_composition:
            allof_members.append(class_composition)

        return {"allOf": allof_members}

    return object_schema


def convert_schema(schema: dict) -> dict[str, dict]:
    """
    Convert all classes and enums in a LinkML schema to a flat
    OpenAPI components/schemas map.
    """
    output: dict[str, dict] = {}

    # Enums first — classes may reference them
    for enum_name in schema.get("enums", {}):
        output[enum_name] = convert_enum(enum_name, schema)

    for class_name in schema.get("classes", {}):
        output[class_name] = convert_class(class_name, schema)

    return output
