#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

TGT_DIR="${ROOT_DIR}/generated/markdown"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  if ! command -v linkml &>/dev/null; then
    echo "The command 'linkml' is missing"
    exit 1
  fi
  if ! command -v mkdocs &>/dev/null; then
    echo "The command 'mkdocs' is missing"
    exit 1
  fi
  RUN=""
fi

mkdir -p "${TGT_DIR}"

${RUN} linkml generate doc \
  --directory="${TGT_DIR}" \
  --template-directory="${ROOT_DIR}/data-model/resources/markdown-templates" \
  --preserve-names \
  --example-directory="${ROOT_DIR}/data-model/resources/examples/valid" \
  "${ROOT_DIR}/data-model/margo-data-model.linkml.yaml"

mkdir -p system-design/data-model
mv generated/markdown/* system-design/data-model/

${RUN} mkdocs build
