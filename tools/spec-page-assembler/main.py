#!/usr/bin/env python3
"""
inject_markdown.py

Replaces <!-- linkml:inject class="ClassName" --> markers in injectable
markdown files with the content of already-generated class markdown files.

Usage:
  python3 inject_markdown.py \
    --input  spec/resources/markdown-manual/injectable/device-capabilities.md \
    --output spec/docs/device-capabilities.md \
    --generated-dir spec/docs/data-models
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Matches: <!-- linkml:inject class="ClassName" -->
# Matches: <!-- linkml:inject example="path/to/file.json" -->
MARKER_RE = re.compile(
    r'<!--\s*linkml:inject\s+(?P<attrs>[^>]+?)\s*-->',
    re.IGNORECASE,
)
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')


def parse_attrs(marker: str) -> dict[str, str]:
    m = MARKER_RE.match(marker.strip())
    return dict(ATTR_RE.findall(m.group("attrs"))) if m else {}


def process_file(
    input_path: Path,
    output_path: Path,
    generated_dir: Path,
) -> bool:
    if not input_path.exists():
        logger.error("Input not found: %s", input_path)
        return False

    source = input_path.read_text(encoding="utf-8")
    errors = 0

    def replace(match: re.Match) -> str:
        nonlocal errors
        raw   = match.group(0)
        attrs = parse_attrs(raw)

        # ── class injection ──────────────────────────────────────────────
        if "class" in attrs:
            class_file = generated_dir / f"{attrs['class']}.md"
            if not class_file.exists():
                logger.error("Generated file not found: %s", class_file)
                errors += 1
                return f"{raw}\n> ⚠️ `{attrs['class']}.md` not found.\n"
            content = class_file.read_text(encoding="utf-8").strip()
            logger.info("  ✓ Injected class: %s", attrs["class"])
            return f"{raw}\n{content}\n"

        # ── example injection ────────────────────────────────────────────
        if "example" in attrs:
            example_file = input_path.parent / attrs["example"]
            if not example_file.exists():
                logger.error("Example not found: %s", example_file)
                errors += 1
                return f"{raw}\n> ⚠️ Example `{attrs['example']}` not found.\n"
            lang    = "json" if example_file.suffix == ".json" else "yaml"
            content = example_file.read_text(encoding="utf-8").strip()
            logger.info("  ✓ Injected example: %s", attrs["example"])
            return f"{raw}\n```{lang}\n{content}\n```\n"

        logger.warning("Unrecognised marker: %s", raw)
        errors += 1
        return raw

    output = MARKER_RE.sub(replace, source)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    if errors:
        logger.warning("⚠️  %d marker(s) failed in %s", errors, input_path)
        return False

    logger.info("Done → %s", output_path)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="inject-markdown",
        description="Inject generated class markdown into injectable markdown files.",
    )
    parser.add_argument("--input",         type=Path, required=True)
    parser.add_argument("--output",        type=Path, required=True)
    parser.add_argument("--generated-dir", type=Path, required=True,
                        help="Directory containing generated class .md files.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    ok = process_file(args.input, args.output, args.generated_dir)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
