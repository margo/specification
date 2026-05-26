from __future__ import annotations

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def load_schema(schema_path: str | Path, base_dir: Path | None = None) -> dict:
    """
    Load a LinkML schema YAML file and recursively resolve its imports.
    Returns a merged schema dict with all classes, enums, types, and slots combined.
    Local definitions take precedence over imported ones.
    """
    schema_path = Path(schema_path)
    base_dir = base_dir or schema_path.parent

    with schema_path.open("r", encoding="utf-8") as f:
        schema: dict = yaml.safe_load(f)

    # Ensure top-level keys always exist
    for key in ("classes", "enums", "types", "slots"):
        schema.setdefault(key, {})

    imports: list[str] = schema.get("imports", [])

    for imp in imports:
        # Skip built-in linkml imports
        if imp.startswith("linkml:"):
            continue

        imp_path = (base_dir / f"{imp}.yaml").resolve()

        if not imp_path.exists():
            logger.warning("Import not found, skipping: %s", imp_path)
            continue

        imported = load_schema(imp_path, base_dir=imp_path.parent)

        # Merge — local definitions take precedence
        schema["classes"] = {**imported["classes"], **schema["classes"]}
        schema["enums"]   = {**imported["enums"],   **schema["enums"]}
        schema["types"]   = {**imported["types"],   **schema["types"]}
        schema["slots"]   = {**imported["slots"],   **schema["slots"]}

    return schema
