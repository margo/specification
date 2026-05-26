#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
CONFIG_FILE="${ROOT_DIR}/tools/configurations/json-schema.config.yaml"

for cmd in yq linkml; do
  command -v "$cmd" >/dev/null || {
    echo "Missing dependency: $cmd"
    exit 1
  }
done

if command -v poetry >/dev/null 2>&1; then
  RUN="poetry run"
else
  RUN=""
fi

length=$(yq '. | length' "$CONFIG_FILE")

for ((i=0; i<length; i++)); do
  name=$(yq -r ".[$i].name" "$CONFIG_FILE")

  schema_rel=$(yq -r ".[$i].input.schema" "$CONFIG_FILE")
  output_rel=$(yq -r ".[$i].output.json_schema" "$CONFIG_FILE")

  schema="${ROOT_DIR}/${schema_rel}"
  output="${ROOT_DIR}/${output_rel}"

  mkdir -p "$(dirname "$output")"

  echo "Generating JSON Schema: ${name}"

  ${RUN} linkml generate json-schema \
    "$schema" \
    > "$output"

  echo "Success -> ${output_rel}"
done