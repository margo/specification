from __future__ import annotations

import logging
from pathlib import Path

from .converter import (
    collect_dependencies,
    extract_definition,
    generate_json_schema,
    rewrite_refs,
)

logger = logging.getLogger(__name__)


def inject_schemas(openapi_doc: dict, template_dir: Path) -> dict:
    """
    Walk all entries in components/schemas.

    For each stub that has ALL of:
      - x-linkml-schema   (path to the LinkML file, relative to template)
      - x-linkml-source   (class or enum name inside that file)

    The tool will:
      1. Resolve the LinkML file path relative to the template directory
      2. Run gen-json-schema on that file (cached per file)
      3. Extract the named class/enum from $defs
      4. Rewrite $refs from #/$defs/X to #/components/schemas/X
      5. Strip [TEMPLATE] prefix from description if present
      6. Rewrite any $refs found in hand-authored preserved fields
      7. Replace the stub in-place, preserving any hand-authored fields
      8. Auto-inject all transitive schema dependencies

    Schemas without x-linkml-schema or x-linkml-source are left untouched.

    Fix #4: Ensures components/schemas exists in the document before
    writing, even if the template omitted it entirely.
    """
    # Fix #4: Use setdefault to ensure components/schemas always exists
    # as a real reference into the document — not a throwaway empty dict.
    openapi_doc.setdefault("components", {}).setdefault("schemas", {})
    schemas: dict = openapi_doc["components"]["schemas"]

    for schema_name, schema_def in list(schemas.items()):
        linkml_file   = schema_def.get("x-linkml-schema")
        linkml_source = schema_def.get("x-linkml-source")

        # Leave hand-authored schemas untouched
        if not linkml_file or not linkml_source:
            logger.debug("Skipping hand-authored schema: %s", schema_name)
            continue

        logger.info(
            "Processing: %s ← %s (%s)",
            schema_name, linkml_source, linkml_file,
        )

        # Resolve path relative to the OpenAPI template's directory
        linkml_path = (template_dir / linkml_file).resolve()

        if not linkml_path.exists():
            logger.error(
                "  ✗ LinkML file not found: %s (referenced by %s)",
                linkml_path, schema_name,
            )
            continue

        # Generate JSON Schema from the LinkML file (cached)
        try:
            json_schema = generate_json_schema(linkml_path)
        except Exception as exc:
            logger.error(
                "  ✗ Failed to generate JSON Schema from %s: %s",
                linkml_path, exc,
            )
            continue

        # Extract the specific class/enum by name.
        # extract_definition() already handles:
        #   - rewrite_refs: #/$defs/X → #/components/schemas/X
        #   - strip_template_prefix: removes [TEMPLATE] from description
        try:
            converted = extract_definition(json_schema, linkml_source)
        except KeyError:
            available = sorted(json_schema.get("$defs", {}).keys())
            logger.error("  ✗ '%s' not found in %s", linkml_source, linkml_file)
            logger.error("    Available: %s", ", ".join(available))
            continue

        # Fix #1: Collect hand-authored fields, then rewrite any $refs
        # they may contain so they point to #/components/schemas/X
        # instead of raw #/$defs/X pointers that would break OpenAPI.
        preserved = {
            k: rewrite_refs(v)
            for k, v in schema_def.items()
            if not k.startswith("x-linkml-")
        }

        # Merge: converted (LinkML-generated) fields are the base,
        # hand-authored preserved fields win on conflict so intentional
        # overrides are respected.
        openapi_doc["components"]["schemas"][schema_name] = {
            **converted,
            **preserved,
        }

        logger.info("  ✓ Injected %s", schema_name)

        # Auto-inject all transitive dependencies.
        # collect_dependencies() already handles rewrite_refs and
        # strip_template_prefix for every dependency schema.
        deps = collect_dependencies(json_schema, linkml_source)
        for dep_name, dep_schema in deps.items():
            if dep_name not in openapi_doc["components"]["schemas"]:
                logger.info("  + Auto-injecting dependency: %s", dep_name)
                openapi_doc["components"]["schemas"][dep_name] = dep_schema
            else:
                logger.debug(
                    "  ~ Dependency already present, skipping: %s", dep_name
                )

    return openapi_doc
