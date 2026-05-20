#!/usr/bin/env bash

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
CONFIG_FILE="${ROOT_DIR}/spec/tools/configurations/uml.config.yml"
KROKI="https://kroki.io/plantuml/"

# Ensure all binary dependencies are present
for cmd in linkml yq curl; do
  command -v "$cmd" &>/dev/null || { echo "Missing dependency: $cmd"; exit 1; }
done

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  RUN=""
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Configuration file not found at $CONFIG_FILE"
  exit 1
fi

# Calculate total array length from the YAML file
length=$(yq '. | length' "$CONFIG_FILE")

# Iterate through every profile using an index-based loop
for ((i=0; i<length; i++)); do
  # 1. Read string values from current object profile index
  name=$(yq -r ".[$i].name" "$CONFIG_FILE")
  schema_rel=$(yq -r ".[$i].schema" "$CONFIG_FILE")
  absolute_schema="${ROOT_DIR}/${schema_rel}"

  if [[ ! -f "$absolute_schema" ]]; then
    echo "Error: Schema file '$absolute_schema' does not exist."
    exit 1
  fi

  # 2. Build the array of individual '--classes_to_render <name>' arguments
  class_args=()
  while IFS= read -r cls; do
    if [[ -n "$cls" && "$cls" != "null" ]]; then
      class_args+=("--classes" "$cls")
    fi
  done < <(yq -r ".[$i].classes_to_render[]" "$CONFIG_FILE" 2>/dev/null || true)

  # 3. Fire the LinkML generator command
  $RUN linkml generate plantuml "${class_args[@]}" "$absolute_schema" > "$TMP"

  # 4. Handle pipeline: Process custom UML injections sequentially
  rel_length=$(yq ".[$i].pipeline | length" "$CONFIG_FILE")
  for ((j=0; j<rel_length; j++)); do
    # Check for explicitly_add_uml_relationship lines
    rel_line=$(yq -r ".[$i].pipeline[$j].explicitly_add_uml_relationship" "$CONFIG_FILE")
    if [[ -n "$rel_line" && "$rel_line" != "null" ]]; then
      # Perform an in-place string append above the diagram terminator
      sed -i "s/@enduml/${rel_line}\n@enduml/" "$TMP"
    fi

    # Check for delete_block operations
    del_pattern=$(yq -r ".[$i].pipeline[$j].delete_uml_block" "$CONFIG_FILE")
    if [[ -n "$del_pattern" && "$del_pattern" != "null" ]]; then
      # Standardise: drop from the matching pattern block line down to closing brace
      sed -i "/${del_pattern}/,/}/d" "$TMP"
    fi
  done

  # 5. Handle output configurations dynamically
  # Extract file extensions (keys) under the output object
  while IFS= read -r fmt; do
    if [[ -n "$fmt" && "$fmt" != "null" ]]; then
      out_rel=$(yq -r ".[$i].output.${fmt}" "$CONFIG_FILE")
      dest_file="${ROOT_DIR}/${out_rel}"

      # Auto-create missing directories cleanly
      mkdir -p "$(dirname "$dest_file")"

      # Stream out to the rendering container layout engine
      curl -sH "Content-Type: text/plain" \
        --data-binary @"$TMP" "${KROKI}/${fmt}" \
        -o "$dest_file"
      echo "Success -> Generated (${fmt^^}): ${out_rel}"
    fi
  done < <(yq -r ".[$i].output | keys[]" "$CONFIG_FILE" 2>/dev/null || true)

done