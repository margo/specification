#!/usr/bin/env bash

# doc generation is around 3-4 steps procecdure
# 1. take linkml
# 2. take markdown templates
# 3. convert linkml to json
# 4. feed this json to markdown templates to render templates to actual docs

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
CONFIG_FILE="${ROOT_DIR}/tools/configurations/markdown.config.yaml"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

EXAMPLES_DIR="${ROOT_DIR}/spec/examples/valid"

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
  template_rel=$(yq -r ".[$i].doc_template_dir" "$CONFIG_FILE")

  schema="${ROOT_DIR}/${schema_rel}"
  template="${ROOT_DIR}/${template_rel}"

  output_md=$(yq -r ".[$i].output.md // empty" "$CONFIG_FILE")
  output_dir=$(yq -r ".[$i].output.directory // empty" "$CONFIG_FILE")

  echo "Generating markdown: ${name}"

  if [[ -n "$output_md" ]]; then
    output_file="${ROOT_DIR}/${output_md}"

    mkdir -p "$(dirname "$output_file")"

    rm -rf "${TMP_DIR:?}"/*

    ${RUN} linkml generate doc \
      --directory="$TMP_DIR" \
      --template-directory="$template" \
      --preserve-names \
      --stacktrace \
      --example-directory="$EXAMPLES_DIR" \
      "$schema"

    mv "${TMP_DIR}/index.md" "$output_file"

    echo "Success -> ${output_md}"
  fi

  if [[ -n "$output_dir" ]]; then
    output_path="${ROOT_DIR}/${output_dir}"

    mkdir -p "$output_path"

    ${RUN} linkml generate doc \
      --directory="$output_path" \
      --template-directory="$template" \
      --preserve-names \
      --stacktrace \
      --example-directory="$EXAMPLES_DIR" \
      "$schema"

    echo "Success -> ${output_dir}"
  fi
done
