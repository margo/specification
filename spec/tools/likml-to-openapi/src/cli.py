from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

from .injector import inject_schemas


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=level,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="linkml-to-openapi",
        description="Fill an OpenAPI template with schemas generated from LinkML sources.",
    )
    parser.add_argument(
        "template",
        type=Path,
        help="Path to the OpenAPI template YAML file",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Path to write the generated OpenAPI YAML file",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    _setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    template_path: Path = args.template.resolve()
    output_path: Path   = args.output.resolve()

    if not template_path.exists():
        logger.error("Template file not found: %s", template_path)
        sys.exit(1)

    logger.info("Loading template: %s", template_path)
    with template_path.open("r", encoding="utf-8") as f:
        openapi_doc: dict = yaml.safe_load(f)

    logger.info("Injecting LinkML schemas...\n")
    filled = inject_schemas(openapi_doc, template_dir=template_path.parent)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(
            filled,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

    logger.info("\nDone → %s", output_path)


if __name__ == "__main__":
    main()
