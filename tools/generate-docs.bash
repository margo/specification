#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "${THIS_DIR}")"

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

TGT_DIR="${ROOT_DIR}/build/artifacts/main-classes"
MERGED_DIR="${ROOT_DIR}/build/site"

mkdir -p "${TGT_DIR}" "${MERGED_DIR}"

cp -R -H "${ROOT_DIR}/docs/"* "${MERGED_DIR}/"
cp -R -H "${ROOT_DIR}/system-design/"* "${MERGED_DIR}/"

# Main classes

for schema_name in "application-description" "application-deployment" "deployment-status" "desired-state-manifest" "device-capabilities" "problem-details"; do
  ${RUN} linkml generate doc \
    --directory="${TMP_DIR}" \
    --template-directory="${ROOT_DIR}/tools/templates/main-classes" \
    --preserve-names \
    --stacktrace \
    --example-directory="${ROOT_DIR}/model/examples/valid" \
    "${ROOT_DIR}/model/${schema_name}.linkml.yaml" >/dev/null

  mv "${TMP_DIR}/index.md" "${TGT_DIR}/${schema_name}.md"
  rm -rf "${TMP_DIR:?}/*"
done

mv "${TGT_DIR}/deployment-status.md" "${MERGED_DIR}/specification/margo-management-interface/"
mv "${TGT_DIR}/device-capabilities.md" "${MERGED_DIR}/specification/margo-management-interface/"
mv "${TGT_DIR}/application-description.md" "${MERGED_DIR}/specification/applications/"
mv "${TGT_DIR}/problem-details.md" "${MERGED_DIR}/specification/"

# Whole Data Model

TGT_DIR="${ROOT_DIR}/build/artifacts/markdown"

mkdir -p "${TGT_DIR}"

${RUN} linkml generate doc \
  --directory="${TGT_DIR}" \
  --template-directory="${ROOT_DIR}/tools/templates/model" \
  --preserve-names \
  --stacktrace \
  --example-directory="${ROOT_DIR}/model/examples/valid" \
  "${ROOT_DIR}/model/margo-data-model.linkml.yaml" >/dev/null

mkdir -p "${MERGED_DIR}/data-model"
mv "${TGT_DIR}"/* "${MERGED_DIR}/data-model/"

"${THIS_DIR}/generate-class-diagram.bash"

mkdir -p "${MERGED_DIR}/figures"
cp "${ROOT_DIR}/build/artifacts/diagrams/DataModel-ClassDiagram.svg" "${MERGED_DIR}/figures/"
cp "${ROOT_DIR}/build/artifacts/diagrams/DataModel-ClassDiagram.png" "${MERGED_DIR}/figures/"

"${THIS_DIR}/generate-openapi.bash"
# generate-openapi.bash writes to both build/artifacts/openapi/ and system-design/.
# Copy the spec into build/site/ so mkdocs build can find it.
cp "${ROOT_DIR}/build/artifacts/openapi/workload-management-api-1.0.0.openapi.yaml" \
  "${MERGED_DIR}/specification/margo-management-interface/workload-management-api-1.0.0.yaml"

# JSON Schemas: copy for download
JSON_SCHEMA_DIR="${ROOT_DIR}/build/artifacts/json-schemas"
MERGED_JSON_SCHEMA_DIR="${MERGED_DIR}/json-schemas"

mkdir -p "${MERGED_JSON_SCHEMA_DIR}"

for schema_file in "${JSON_SCHEMA_DIR}"/*.schema.json; do
  if [ -f "${schema_file}" ]; then
    cp "${schema_file}" "${MERGED_JSON_SCHEMA_DIR}/"
  fi
done
