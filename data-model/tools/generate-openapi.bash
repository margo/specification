#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

TMPL="${ROOT_DIR}/data-model/tools/workload-management-api-1.0.0.openapi.yaml"
TGT_DIR="${ROOT_DIR}/generated/openapi"
TGT_FILE="${TGT_DIR}/$(basename "${TMPL}")"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  if ! command -v linkml &>/dev/null; then
    echo "The command 'linkml' is missing"
    exit 1
  fi
  if ! command -v yq &>/dev/null; then
    echo "The command 'yq' is missing"
    exit 1
  fi
  RUN=""
fi

mkdir -p "${TGT_DIR}"
cp "${TMPL}" "${TGT_FILE}"

${RUN} python "${THIS_DIR}/openapigen.py" \
  --template "${THIS_DIR}/workload-management-api-1.0.0.openapi.yaml" \
  "${ROOT_DIR}/data-model/margo-data-model.linkml.yaml" \
  >"${TGT_FILE}"
