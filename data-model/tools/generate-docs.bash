#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -r "${TMP_DIR}"
}

trap cleanup EXIT

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

TGT_DIR="${ROOT_DIR}/generated/markdown_main-classes"

mkdir -p "${TGT_DIR}"

# Main classes

for schema_name in "application-description" "application-deployment" "deployment-status" "desired-state-manifest" "device-capabilities"; do
  ${RUN} linkml generate doc \
    --directory="${TMP_DIR}" \
    --template-directory="${ROOT_DIR}/data-model/resources/markdown-templates_main-classes" \
    --preserve-names \
    --stacktrace \
    --example-directory="${ROOT_DIR}/data-model/resources/examples/valid" \
    "${ROOT_DIR}/data-model/${schema_name}.linkml.yaml"

  mv "${TMP_DIR}/index.md" "${TGT_DIR}/${schema_name}.md"
  rm -rf "${TMP_DIR:?}/*"
done

TGT_DIR="${ROOT_DIR}/generated/markdown"

mkdir -p "${TGT_DIR}"

# Whole Data Model

${RUN} linkml generate doc \
  --directory="${TGT_DIR}" \
  --template-directory="${ROOT_DIR}/data-model/resources/markdown-templates" \
  --preserve-names \
  --stacktrace \
  --example-directory="${ROOT_DIR}/data-model/resources/examples/valid" \
  "${ROOT_DIR}/data-model/margo-data-model.linkml.yaml"

mkdir -p system-design/data-model
mv generated/markdown/* system-design/data-model/

"${THIS_DIR}/generate-class-diagram.bash"

cp "${ROOT_DIR}/generated/diagrams/DataModel-ClassDiagram.svg" system-design/figures/
cp "${ROOT_DIR}/generated/diagrams/DataModel-ClassDiagram.png" system-design/figures/

"${THIS_DIR}/generate-openapi.bash"

${RUN} mkdocs build
