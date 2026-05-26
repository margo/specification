from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

from .converter import generate_json_schema
from .injector import inject_schemas


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=level,
    )
    # Always suppress noisy LinkML internals unless explicitly in verbose mode
    if not verbose:
        logging.getLogger("linkml").setLevel(logging.WARNING)
        logging.getLogger("linkml_runtime").setLevel(logging.WARNING)
        logging.getLogger("rdflib").setLevel(logging.WARNING)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="linkml-to-openapi",
        description=(
            "Inject OpenAPI schemas generated from LinkML source files "
            "into an OpenAPI template. Each schema stub references its "
            "own LinkML file via x-linkml-schema."
        ),
    )
    parser.add_argument(
        "template",
        type=Path,
        nargs="?",           # Fix #5: optional — not needed for --list-definitions
        default=None,
        help=(
            "Path to the OpenAPI template YAML file. "
            "Required unless --list-definitions is used."
        ),
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",           # Fix #5: optional — not needed for --list-definitions
        default=None,
        help=(
            "Path to write the generated OpenAPI YAML file. "
            "Required unless --list-definitions is used."
        ),
    )
    parser.add_argument(
        "--list-definitions",
        metavar="LINKML_FILE",
        help=(
            "List all available class/enum names in the given LinkML file "
            "and exit. Useful for finding the correct x-linkml-source value. "
            "When this flag is used, 'template' and 'output' are not required."
        ),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def _cmd_list_definitions(linkml_file: str, logger: logging.Logger) -> None:
    """
    Handle the --list-definitions mode.

    Resolves the given LinkML file, generates its JSON Schema,
    and prints all available class/enum definition names to stdout.
    Exits with code 1 if the file is not found or generation fails.
    """
    linkml_path = Path(linkml_file).resolve()

    if not linkml_path.exists():
        logger.error("LinkML file not found: %s", linkml_path)
        sys.exit(1)

    try:
        json_schema = generate_json_schema(linkml_path)
    except Exception as exc:
        logger.error("Failed to generate JSON Schema from %s: %s", linkml_path, exc)
        sys.exit(1)

    defs = sorted(json_schema.get("$defs", {}).keys())

    if not defs:
        print(f"\nNo definitions found in {linkml_path.name}.\n")
    else:
        print(f"\nAvailable definitions in {linkml_path.name}:\n")
        for name in defs:
            print(f"  - {name}")
        print()

    sys.exit(0)


def _cmd_inject(
    template: Path | None,
    output: Path | None,
    logger: logging.Logger,
) -> None:
    """
    Handle the main inject mode.

    Validates that both 'template' and 'output' were provided,
    loads the OpenAPI template, runs schema injection, and writes
    the result to the output path.
    Exits with code 1 on any validation or processing error.
    """
    # Fix #5: Validate that both required positional args are present
    # when not in --list-definitions mode, and emit clear error messages.
    missing = []
    if template is None:
        missing.append("'template'")
    if output is None:
        missing.append("'output'")

    if missing:
        logger.error(
            "The following arguments are required for injection mode: %s",
            ", ".join(missing),
        )
        logger.error(
            "Usage: linkml-to-openapi <template> <output> [-v]"
        )
        sys.exit(1)

    template_path = template.resolve()
    output_path   = output.resolve()

    if not template_path.exists():
        logger.error("Template file not found: %s", template_path)
        sys.exit(1)

    logger.info("Loading template: %s", template_path)
    try:
        with template_path.open("r", encoding="utf-8") as f:
            openapi_doc: dict = yaml.safe_load(f)
    except Exception as exc:
        logger.error("Failed to load template %s: %s", template_path, exc)
        sys.exit(1)

    if not isinstance(openapi_doc, dict):
        logger.error(
            "Template file did not parse to a YAML mapping: %s", template_path
        )
        sys.exit(1)

    filled = inject_schemas(openapi_doc, template_dir=template_path.parent)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("w", encoding="utf-8") as f:
            yaml.dump(
                filled,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            )
    except Exception as exc:
        logger.error("Failed to write output to %s: %s", output_path, exc)
        sys.exit(1)

    logger.info("Done → %s", output_path)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    _setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if args.list_definitions:
        _cmd_list_definitions(args.list_definitions, logger)
    else:
        _cmd_inject(args.template, args.output, logger)


if __name__ == "__main__":
    main()