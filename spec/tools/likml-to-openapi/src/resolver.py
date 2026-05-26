from __future__ import annotations

import logging
from typing import Literal, TypedDict

from .types import LINKML_TYPE_MAP, XSD_TYPE_MAP, COMPOSITION_MAP

logger = logging.getLogger(__name__)


class ResolvedRange(TypedDict):
    kind: Literal["scalar", "enum", "class"]
    schema: dict        # populated for scalar
    name: str | None    # populated for enum / class


def resolve_range(range_name: str | None, schema: dict) -> ResolvedRange:
    """
    Determine whether a range name refers to:
      - a built-in LinkML scalar type
      - a user-defined type alias
      - a user-defined enum
      - a user-defined class
    """
    if not range_name:
        return ResolvedRange(kind="scalar", schema={"type": "string"}, name=None)

    # Built-in scalar
    if range_name in LINKML_TYPE_MAP:
        return ResolvedRange(
            kind="scalar",
            schema=dict(LINKML_TYPE_MAP[range_name]),
            name=None,
        )

    # User-defined type alias (e.g. from types.linkml)
    if range_name in schema.get("types", {}):
        type_def = schema["types"][range_name]
        if "uri" in type_def:
            base = XSD_TYPE_MAP.get(type_def["uri"], {"type": "string"})
        elif "typeof" in type_def:
            base = resolve_range(type_def["typeof"], schema)["schema"]
        else:
            base = {"type": "string"}
        return ResolvedRange(kind="scalar", schema=dict(base), name=None)

    # Enum
    if range_name in schema.get("enums", {}):
        return ResolvedRange(kind="enum", schema={}, name=range_name)

    # Class
    if range_name in schema.get("classes", {}):
        return ResolvedRange(kind="class", schema={}, name=range_name)

    logger.warning("Unknown range '%s' — defaulting to string", range_name)
    return ResolvedRange(kind="scalar", schema={"type": "string"}, name=None)


def resolve_union_expr(
    expr: dict | list,
    schema: dict,
    openapi_keyword: str,
) -> dict:
    """
    Resolve a LinkML union expression (any_of, all_of, exactly_one_of, none_of)
    into an OpenAPI composition schema.

    LinkML union expressions are lists of anonymous range expressions:
      any_of:
        - range: string
        - range: integer
        - range: MyClass

    Each item may itself carry constraints (pattern, minimum_value, etc.)
    which are resolved recursively.

    Returns an OpenAPI schema fragment:
      { "anyOf": [ { "type": "string" }, { "type": "integer" }, { "$ref": "..." } ] }
    """
    from .converter import _build_range_schema  # local import to avoid circular

    if not isinstance(expr, list):
        expr = [expr]

    members = []
    for item in expr:
        if not isinstance(item, dict):
            continue

        range_name = item.get("range")
        resolved   = resolve_range(range_name, schema)
        member     = _build_range_schema(resolved, item, schema, visited=set())

        # Apply inline constraints on the member
        from .converter import _apply_scalar_constraints
        if resolved["kind"] == "scalar":
            _apply_scalar_constraints(member, item)

        members.append(member)

    if openapi_keyword == "not":
        # OpenAPI 'not' takes a single schema — wrap in anyOf if multiple
        return {"not": members[0] if len(members) == 1 else {"anyOf": members}}

    return {openapi_keyword: members}


def collect_attributes(class_name: str, schema: dict) -> dict:
    """
    Collect all attributes for a class, walking the is_a inheritance chain
    and merging any mixins. Local attributes override inherited ones.
    """
    class_def = schema["classes"].get(class_name)
    if not class_def:
        return {}

    inherited: dict = {}

    # Walk is_a chain
    if "is_a" in class_def:
        inherited = collect_attributes(class_def["is_a"], schema)

    # Merge mixins (left to right)
    for mixin in class_def.get("mixins", []):
        inherited = {**inherited, **collect_attributes(mixin, schema)}

    # Local attributes override inherited
    local = class_def.get("attributes", {})
    return {**inherited, **local}
