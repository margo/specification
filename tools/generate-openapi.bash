#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "${THIS_DIR}")"

TGT_DIR="${ROOT_DIR}/build/artifacts/openapi"
TGT_FILE="${TGT_DIR}/workload-management-api-1.0.0-rc.2.openapi.yaml"

# Tracked location in system-design/ — this is what the repo uses
# generate-docs.bash copies system-design/ into build/site/ for mkdocs
SYSTEM_DESIGN_FILE="${ROOT_DIR}/system-design/specification/margo-management-interface/workload-management-api-1.0.0-rc.2.yaml"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  if ! command -v linkml &>/dev/null; then
    echo "The command 'linkml' is missing"
    exit 1
  fi
  RUN=""
fi

mkdir -p "${TGT_DIR}"

# TODO: remove following block after LinkML release >v1.11.1
(
  cd "${THIS_DIR}"
  ${RUN} python openapigen.py --keep-unreferenced --inline-enums -t templates/openapi/workload-management-api-1.0.0-rc.2.openapi.yaml ../model/margo-data-model.linkml.yaml \
    >"${TGT_FILE}"
  cp "${TGT_FILE}" "${SYSTEM_DESIGN_FILE}"
)
exit

${RUN} linkml generate openapi \
  --template "${THIS_DIR}/templates/openapi/workload-management-api-1.0.0-rc.2.openapi.yaml" \
  --inline-enums \
  --keep-unreferenced \
  "${ROOT_DIR}/model/margo-data-model.linkml.yaml" \
  >"${TGT_FILE}"

# Copy to the tracked location in system-design/ so it is picked up by
# generate-docs.bash (which copies system-design/ → build/site/) and by git
cp "${TGT_FILE}" "${SYSTEM_DESIGN_FILE}"
