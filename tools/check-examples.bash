#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
CONFIG_FILE="${ROOT_DIR}/tools/configurations/examples.config.yaml"

VERBOSITY="${1:-info}"

log() {
  local level="$1"
  shift

  case "$VERBOSITY:$level" in
    trace:*|debug:debug|debug:info|info:info)
      echo "$@"
      ;;
  esac
}

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

validate_examples() {
  local schema="$1"
  local target_class="$2"
  local expected="$3"
  shift 3

  for example in "$@"; do
    [[ -f "$example" ]] || continue

    if result=$(
      ${RUN} linkml validate \
        --schema "$schema" \
        --target-class "$target_class" \
        "$example" 2>&1
    ); then
      success=true
    else
      success=false
    fi

    if [[ "$expected" == "valid" && "$success" == true ]]; then
      echo "✅ Valid example got successfully passed (${example})"

    elif [[ "$expected" == "invalid" && "$success" == false ]]; then
      echo "✅ Invalid example got successfully flagged (${example})"

    else
      echo " Validation mismatch (${example})"
      echo "$result"
      exit 1
    fi
  done
}

length=$(yq '. | length' "$CONFIG_FILE")

for ((i=0; i<length; i++)); do
  name=$(yq -r ".[$i].name" "$CONFIG_FILE")

  schema_rel=$(yq -r ".[$i].schema" "$CONFIG_FILE")
  target_class=$(yq -r ".[$i].target_class" "$CONFIG_FILE")

  valid_rel=$(yq -r ".[$i].examples.valid" "$CONFIG_FILE")
  invalid_rel=$(yq -r ".[$i].examples.invalid" "$CONFIG_FILE")

  schema="${ROOT_DIR}/${schema_rel}"
  valid_dir="${ROOT_DIR}/${valid_rel}"
  invalid_dir="${ROOT_DIR}/${invalid_rel}"

  log info "Checking: ${name}"

  validate_examples \
    "$schema" \
    "$target_class" \
    valid \
    "${valid_dir}/${target_class}-"*.yaml \
    "${valid_dir}/${target_class}-"*.json

  validate_examples \
    "$schema" \
    "$target_class" \
    invalid \
    "${invalid_dir}/${target_class}-"*.yaml \
    "${invalid_dir}/${target_class}-"*.json
done