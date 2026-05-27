#!/usr/bin/env bash
# generate-spec-pages.bash
#
# Processes all spec pages in spec/templates/spec-pages/ by injecting
# generated class pages into <!-- linkml:inject --> markers.
#
# Prerequisites:
#   - generate-class-pages.bash must have run first
#   - main.py must be available in tools/spec-page-assembler
#
# Usage:
#   ./generate-spec-pages.bash
#   ./generate-spec-pages.bash -v    # verbose output

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPEC_DIR="$(cd "${SCRIPT_DIR}/../spec" && pwd)"

INPUT_DIR="${SPEC_DIR}/templates/spec-pages"
GENERATED_CLASS_PAGES_DIR="${SPEC_DIR}/generated/class-pages"
OUTPUT_DIR="${SPEC_DIR}/generated/spec-pages"
INJECT_SCRIPT="${SCRIPT_DIR}/spec-page-assembler/main.py"

# ─────────────────────────────────────────────────────────────────────────────
# Args
# ─────────────────────────────────────────────────────────────────────────────

VERBOSE=""
while getopts "v" opt; do
  case $opt in
    v) VERBOSE="-v" ;;
    *) echo "Usage: $0 [-v]" && exit 1 ;;
  esac
done

# ─────────────────────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────────────────────

if [[ ! -d "${INPUT_DIR}" ]]; then
  echo "ERROR: spec-pages template directory not found: ${INPUT_DIR}"
  exit 1
fi

if [[ ! -d "${GENERATED_CLASS_PAGES_DIR}" ]]; then
  echo "ERROR: Generated class pages not found: ${GENERATED_CLASS_PAGES_DIR}"
  echo "       Run generate-class-pages.bash first."
  exit 1
fi

if [[ ! -f "${INJECT_SCRIPT}" ]]; then
  echo "ERROR: main.py not found: ${INJECT_SCRIPT}"
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
# Process
# ─────────────────────────────────────────────────────────────────────────────

mkdir -p "${OUTPUT_DIR}"

echo "Generating spec pages..."
echo "  Input:         ${INPUT_DIR}"
echo "  Class pages:   ${GENERATED_CLASS_PAGES_DIR}"
echo "  Output:        ${OUTPUT_DIR}"
echo ""

SUCCESS=0
FAILURE=0

while IFS= read -r input_file; do
  # Preserve subdirectory structure relative to INPUT_DIR
  relative="${input_file#${INPUT_DIR}/}"
  output_file="${OUTPUT_DIR}/${relative}"

  mkdir -p "$(dirname "${output_file}")"

  [[ -n "${VERBOSE}" ]] && echo "  Processing: ${relative}"

  if python3 "${INJECT_SCRIPT}" \
      --input         "${input_file}" \
      --output        "${output_file}" \
      --generated-dir "${GENERATED_CLASS_PAGES_DIR}" \
      ${VERBOSE}; then
    SUCCESS=$((SUCCESS + 1))
  else
    FAILURE=$((FAILURE + 1))
    echo "  ✗ Failed: ${relative}"
    exit 1
  fi
done < <(find "${INPUT_DIR}" -name "*.md" | sort)

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "Done: ${SUCCESS} succeeded, ${FAILURE} failed."

if [[ ${FAILURE} -gt 0 ]]; then
  exit 1
fi