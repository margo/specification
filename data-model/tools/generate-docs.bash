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
MERGED_DIR="${ROOT_DIR}/merged"

mkdir -p "${TGT_DIR}" "${MERGED_DIR}"

cp -R -H "${ROOT_DIR}/system-design/"* "${MERGED_DIR}/"

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

mv "${TGT_DIR}/deployment-status.md" "${MERGED_DIR}/specification/margo-management-interface/"
mv "${TGT_DIR}/device-capabilities.md" "${MERGED_DIR}/specification/margo-management-interface/"
mv "${TGT_DIR}/application-description.md" "${MERGED_DIR}/specification/applications/"

# Whole Data Model

TGT_DIR="${ROOT_DIR}/generated/markdown"

mkdir -p "${TGT_DIR}"

${RUN} linkml generate doc \
  --directory="${TGT_DIR}" \
  --template-directory="${ROOT_DIR}/data-model/resources/markdown-templates" \
  --preserve-names \
  --stacktrace \
  --example-directory="${ROOT_DIR}/data-model/resources/examples/valid" \
  "${ROOT_DIR}/data-model/margo-data-model.linkml.yaml"

mkdir -p system-design/data-model
mv generated/markdown/* "${MERGED_DIR}/data-model/"

"${THIS_DIR}/generate-class-diagram.bash"

cp "${ROOT_DIR}/generated/diagrams/DataModel-ClassDiagram.svg" "${MERGED_DIR}/figures/"
cp "${ROOT_DIR}/generated/diagrams/DataModel-ClassDiagram.png" "${MERGED_DIR}/figures/"

"${THIS_DIR}/generate-openapi.bash"
mv "${ROOT_DIR}/generated/openapi/workload-management-api-1.0.0.openapi.yaml" "${MERGED_DIR}/specification/margo-management-interface/workload-management-api-1.0.0.yaml"

${RUN} mkdocs build
