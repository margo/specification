from __future__ import annotations

import logging
from pathlib import Path

from .converter import convert_class, convert_enum
from .loader import load_schema

logger = logging.getLogger(__name__)

TEMPLATE_PREFIX = "[TEMPLATE]"


def inject_schemas(openapi_doc: dict, template_dir: Path) -> dict:
    """
    Walk all entries in components/schemas.
    For each stub with x-linkml-schema + x-linkml-source:
      1. Load the referenced LinkML file (cached)
      2. Convert the target class or enum
      3. Replace the stub in-place, preserving any manually authored fields
    """
    schemas: dict = openapi_doc.get("components", {}).get("schemas", {})
    schema_cache: dict[str, dict] = {}

    for schema_name, schema_def in schemas.items():
        linkml_file   = schema_def.get("x-linkml-schema")
        linkml_source = schema_def.get("x-linkml-source")
        source_type   = schema_def.get("x-linkml-source-type", "class")

        if not linkml_file or not linkml_source:
            continue

        logger.info(
            "Processing: %s ← %s (%s)", schema_name, linkml_source, linkml_file
        )

        # Load & cache
        full_path = (template_dir / linkml_file).resolve()
        if str(full_path) not in schema_cache:
            schema_cache[str(full_path)] = load_schema(full_path)

        linkml_schema = schema_cache[str(full_path)]

        # Convert
        try:
            if source_type == "enum":
                if linkml_source not in linkml_schema.get("enums", {}):
                    logger.warning(
                        "Enum '%s' not found in %s — skipping",
                        linkml_source, linkml_file,
                    )
                    continue
                converted = convert_enum(linkml_source, linkml_schema)

            else:  # default: class
                if linkml_source not in linkml_schema.get("classes", {}):
                    logger.warning(
                        "Class '%s' not found in %s — skipping",
                        linkml_source, linkml_file,
                    )
                    continue
                converted = convert_class(linkml_source, linkml_schema)

        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to convert '%s': %s", schema_name, exc)
            continue

        # Strip [TEMPLATE] prefix from description
        if "description" in converted:
            converted["description"] = converted["description"].removeprefix(
                TEMPLATE_PREFIX
            ).strip()

        # Preserve manually authored non-x-linkml fields
        preserved = {
            k: v
            for k, v in schema_def.items()
            if not k.startswith("x-linkml-") and k != "description"
        }

        openapi_doc["components"]["schemas"][schema_name] = {
            **converted,
            **preserved,
        }

        logger.info("  ✓ Injected %s", schema_name)

    return openapi_doc
