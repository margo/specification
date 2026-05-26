#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
CONFIG_FILE="${ROOT_DIR}/spec/tools/configurations/openapi.config.yaml"

# ── Dependency checks ────────────────────────────────────────────────────────
for cmd in yq python3; do
  command -v "$cmd" >/dev/null || {
    echo "Missing dependency: $cmd"
    exit 1
  }
done

# ── Runner: prefer poetry if available ───────────────────────────────────────
if command -v poetry >/dev/null 2>&1; then
  RUN="poetry run"
else
  RUN=""
fi

# ── Optional verbose flag: pass -v to enable debug logging ───────────────────
VERBOSE=""
for arg in "$@"; do
  case "$arg" in
    -v|--verbose) VERBOSE="--verbose" ;;
    *)
      echo "Unknown argument: $arg"
      echo "Usage: $(basename "$0") [-v|--verbose]"
      exit 1
      ;;
  esac
done

# ── Process each entry in the config ─────────────────────────────────────────
length=$(yq '. | length' "$CONFIG_FILE")

if [[ "$length" -eq 0 ]]; then
  echo "No entries found in config: $CONFIG_FILE"
  exit 1
fi

success=0
failure=0

for ((i=0; i<length; i++)); do
  name=$(yq -r ".[$i].name" "$CONFIG_FILE")

  template_rel=$(yq -r ".[$i].input.template" "$CONFIG_FILE")
  output_rel=$(yq -r ".[$i].output.yaml"     "$CONFIG_FILE")

  template="${ROOT_DIR}/${template_rel}"
  output="${ROOT_DIR}/${output_rel}"

  # Validate that the template file exists before invoking the tool
  if [[ ! -f "$template" ]]; then
    echo "ERROR: Template not found for '${name}': ${template}"
    ((failure++)) || true
    continue
  fi

  echo "Generating OpenAPI: ${name}"
  echo "  template → ${template_rel}"
  echo "  output   → ${output_rel}"

  mkdir -p "$(dirname "$output")"

  # Invoke the linkml-to-openapi CLI.
  # The tool writes directly to <output> — no stdout redirection needed.
  if ${RUN} linkml-to-openapi \
      ${VERBOSE} \
      "$template" \
      "$output"; then
    echo "  ✓ Success → ${output_rel}"
    ((success++)) || true
  else
    echo "  ✗ Failed  → ${output_rel}"
    ((failure++)) || true
  fi

done

# ── Final summary ─────────────────────────────────────────────────────────────
echo ""
echo "Done: ${success} succeeded, ${failure} failed."

if [[ "$failure" -gt 0 ]]; then
  exit 1
fi
