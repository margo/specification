from __future__ import annotations

import json
import logging
from pathlib import Path

from linkml.generators.jsonschemagen import JsonSchemaGenerator

logger = logging.getLogger(__name__)
logging.getLogger("linkml.generators.jsonschemagen").setLevel(logging.WARNING)
logging.getLogger("linkml_runtime").setLevel(logging.WARNING)
logging.getLogger("linkml").setLevel(logging.WARNING)

# Cache so we don't re-run gen-json-schema on the same file twice
_schema_cache: dict[str, dict] = {}

# Prefix used in LinkML descriptions to mark template-only entries
TEMPLATE_PREFIX = "[TEMPLATE]"


def generate_json_schema(linkml_path: str | Path) -> dict:
    """
    Run LinkML's built-in JSON Schema generator against a LinkML file
    and return the parsed output as a dict.

    Results are cached by resolved path so the same file is only
    processed once per tool invocation even if multiple stubs
    reference it.
    """
    key = str(Path(linkml_path).resolve())

    if key not in _schema_cache:
        logger.debug("Running gen-json-schema on: %s", linkml_path)
        generator = JsonSchemaGenerator(str(linkml_path))
        raw = generator.serialize()
        _schema_cache[key] = json.loads(raw)
    else:
        logger.debug("Cache hit for: %s", linkml_path)

    return _schema_cache[key]


def extract_definition(json_schema: dict, name: str) -> dict:
    """
    Extract a single class or enum definition by name from the
    $defs block of a generated JSON Schema document.

    Raises KeyError with a helpful message if the name is not found.

    The returned schema has, in order:
      1. $refs rewritten from #/$defs/X → #/components/schemas/X
      2. $ref siblings wrapped in allOf for OAS 3.0 compliance
      3. Nullable arrays/anyOf patterns normalised to nullable: true
      4. [TEMPLATE] prefix stripped from description (if present)
    """
    defs = json_schema.get("$defs", {})

    if name not in defs:
        available = ", ".join(sorted(defs.keys()))
        raise KeyError(
            f"'{name}' not found in generated schema.\n"
            f"Available definitions: {available}"
        )

    schema = rewrite_refs(defs[name])
    schema = normalize_nullable(schema)
    return strip_template_prefix(schema)


def collect_dependencies(
    json_schema: dict,
    name: str,
    visited: set[str] | None = None,
) -> dict[str, dict]:
    """
    Recursively collect all $defs entries that a given definition
    depends on via $ref, so they can all be injected into
    components/schemas and resolved correctly.

    Returns a flat dict of { name: schema } for all dependencies
    excluding the root definition itself.

    Each returned schema has, in order:
      1. $refs rewritten from #/$defs/X → #/components/schemas/X
      2. $ref siblings wrapped in allOf for OAS 3.0 compliance
      3. Nullable arrays/anyOf patterns normalised to nullable: true
      4. [TEMPLATE] prefix stripped from description (if present)

    Note: rewrite_refs is idempotent — refs already pointing to
    #/components/schemas/X are left unchanged, so calling this
    function multiple times on the same schema is safe.

    Note: _find_refs always operates on the raw (pre-rewrite) defs
    so that #/$defs/ pointers are reliably discovered before any
    rewriting takes place.
    """
    visited = visited or set()
    if name in visited:
        return {}
    visited.add(name)

    defs = json_schema.get("$defs", {})
    if name not in defs:
        return {}

    result: dict[str, dict] = {}

    # Search for $refs in the *original* (non-rewritten) defs entry
    # so we always resolve against #/$defs/ pointers from the source.
    refs = _find_refs(defs[name])

    for ref in refs:
        if ref.startswith("#/$defs/"):
            dep_name = ref.removeprefix("#/$defs/")
            if dep_name not in visited:
                dep_schema = rewrite_refs(defs[dep_name])
                dep_schema = normalize_nullable(dep_schema)
                dep_schema = strip_template_prefix(dep_schema)
                result[dep_name] = dep_schema

                # Recurse into the dependency's own dependencies
                result.update(
                    collect_dependencies(json_schema, dep_name, visited)
                )

    return result


def strip_template_prefix(schema: dict) -> dict:
    """
    Strip the [TEMPLATE] prefix from the 'description' field of a schema
    dict, if present. Returns the schema dict with the description cleaned.

    This is applied uniformly to both root schemas and auto-injected
    dependency schemas to prevent the prefix from leaking into output.
    """
    if "description" in schema and isinstance(schema["description"], str):
        schema = {
            **schema,
            "description": schema["description"]
            .removeprefix(TEMPLATE_PREFIX)
            .strip(),
        }
    return schema


def normalize_nullable(schema: dict | list | str) -> dict | list | str:
    """
    Normalise JSON Schema nullable patterns into OpenAPI 3.0.x equivalents.

    OpenAPI 3.0.x does not support:
      - type: [X, 'null']          (JSON Schema array types)
      - anyOf: [{...}, {type: null}]  (JSON Schema null union)

    Both are converted to the OAS 3.0 idiomatic form:
      - type: X + nullable: true

    Rules applied, in order:

    1. type: [X, 'null']
         → type: X, nullable: true
       type: ['null']
         → nullable: true  (type key removed entirely)
       type: [X, Y, 'null']  (multiple non-null types)
         → anyOf: [{type: X}, {type: Y}], nullable: true

    2. anyOf: [{$ref: '#/components/schemas/Foo'}, {type: 'null'}]
         → allOf: [{$ref: '...'}], nullable: true
       anyOf: [{...schema...}, {type: 'null'}]
         → the sole non-null schema is inlined, nullable: true
       anyOf: [{A}, {B}, {type: 'null'}]
         → anyOf: [{A}, {B}], nullable: true

    Recursion is applied depth-first so nested schemas are also normalised.
    """
    if isinstance(schema, list):
        return [normalize_nullable(item) for item in schema]

    if not isinstance(schema, dict):
        return schema

    # Recurse depth-first into all values before applying rules at this level
    result: dict = {k: normalize_nullable(v) for k, v in schema.items()}

    # ------------------------------------------------------------------ #
    # Rule 1: type: [X, 'null', ...]  →  type: X + nullable: true        #
    # ------------------------------------------------------------------ #
    if "type" in result and isinstance(result["type"], list):
        types: list = result["type"]
        non_null = [t for t in types if t != "null"]
        has_null = len(non_null) < len(types)

        if has_null:
            result["nullable"] = True

        if len(non_null) == 0:
            # type: ['null'] — remove type entirely, keep nullable: true
            del result["type"]
        elif len(non_null) == 1:
            # type: [X, 'null'] — simplest and most common case
            result["type"] = non_null[0]
        else:
            # type: [X, Y, ..., 'null'] — multiple non-null types
            # Represent as anyOf since OAS 3.0 doesn't allow type arrays
            del result["type"]
            existing_anyof = result.get("anyOf", [])
            result["anyOf"] = existing_anyof + [{"type": t} for t in non_null]

    # ------------------------------------------------------------------ #
    # Rule 2: anyOf: [{...}, {type: 'null'}]  →  inline + nullable: true #
    # ------------------------------------------------------------------ #
    if "anyOf" in result and isinstance(result["anyOf"], list):
        anyof: list = result["anyOf"]
        null_schemas     = [s for s in anyof if isinstance(s, dict) and s.get("type") == "null"]
        non_null_schemas = [s for s in anyof if not (isinstance(s, dict) and s.get("type") == "null")]
        has_null = bool(null_schemas)

        if has_null:
            result["nullable"] = True

            if len(non_null_schemas) == 0:
                # anyOf: [{type: null}] — degenerate, remove anyOf entirely
                del result["anyOf"]

            elif len(non_null_schemas) == 1:
                sole = non_null_schemas[0]
                del result["anyOf"]

                if "$ref" in sole:
                    # anyOf: [{$ref: '...'}, {type: null}]
                    # → allOf: [{$ref: '...'}], nullable: true
                    # allOf is required because $ref must not have siblings
                    # in OAS 3.0, and nullable is now a sibling.
                    result["allOf"] = [sole]
                else:
                    # anyOf: [{inline schema}, {type: null}]
                    # → inline the schema fields directly, nullable: true
                    # Existing keys in result take priority (e.g. description)
                    for k, v in sole.items():
                        if k not in result:
                            result[k] = v
            else:
                # anyOf: [{A}, {B}, ..., {type: null}]
                # → anyOf: [{A}, {B}, ...], nullable: true
                result["anyOf"] = non_null_schemas

    return result


def _find_refs(obj: dict | list | str) -> list[str]:
    """
    Recursively find all $ref values in a schema object.

    Always searches the raw (pre-rewrite) structure so that
    #/$defs/ pointers are reliably discovered before any rewriting
    takes place.
    """
    refs = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str):
                refs.append(v)
            else:
                refs.extend(_find_refs(v))
    elif isinstance(obj, list):
        for item in obj:
            refs.extend(_find_refs(item))
    return refs


def rewrite_refs(schema: dict | list | str) -> dict | list | str:
    """
    Recursively rewrite all local JSON Schema $ref pointers:
      "#/$defs/MyClass"  →  "#/components/schemas/MyClass"

    OpenAPI 3.0.x does not allow any keywords to appear alongside a $ref
    (siblings are silently ignored by validators and tooling). When a dict
    contains both a $ref and other keywords (e.g. description), the $ref
    is wrapped in allOf so the siblings remain valid:

      {$ref: '...', description: '...'}
        →  {allOf: [{$ref: '...'}], description: '...'}

    This function is idempotent:
      - Refs already pointing to #/components/schemas/X are left unchanged.
      - allOf wrapping is only applied when siblings are actually present.
      - Safe to call multiple times on the same schema.

    Also strips keywords not valid in OpenAPI 3.0.x:
      - `const`  (JSON Schema draft-7, not in OpenAPI 3.0)
        equals_string is already captured by `enum: [value]`
    """
    if isinstance(schema, dict):
        # Strip `const` before any further processing
        schema = {k: v for k, v in schema.items() if k != "const"}

        if "$ref" in schema:
            ref_value = _rewrite_ref_value(schema["$ref"])
            siblings  = {k: v for k, v in schema.items() if k != "$ref"}

            if siblings:
                # Wrap $ref in allOf so siblings are valid in OAS 3.0
                return {
                    "allOf": [{"$ref": ref_value}],
                    **{k: rewrite_refs(v) for k, v in siblings.items()},
                }
            return {"$ref": ref_value}

        # No $ref at this level — recurse into all values
        return {k: rewrite_refs(v) for k, v in schema.items()}

    if isinstance(schema, list):
        return [rewrite_refs(item) for item in schema]

    return schema


def _rewrite_ref_value(ref: str) -> str:
    """
    Rewrite a single $ref value from JSON Schema format to OpenAPI format.

    Idempotent: refs not starting with #/$defs/ are returned unchanged,
    which means already-rewritten #/components/schemas/ refs are safe.
    """
    if ref.startswith("#/$defs/"):
        name = ref.removeprefix("#/$defs/")
        return f"#/components/schemas/{name}"
    return ref
