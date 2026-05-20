#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(git rev-parse --show-toplevel)"

TMPL="${ROOT_DIR}/spec/tools/workload-management-api.openapi.template.yaml"
TGT_DIR="${ROOT_DIR}/spec/generated/openapi"
TGT_FILE="${TGT_DIR}/$(basename "${TMPL}")"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
  poetry install
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

${RUN} python3 "${THIS_DIR}/openapigen.py" \
  --template "${THIS_DIR}/workload-management-api.openapi.template.yaml" \
  "${ROOT_DIR}/spec/data-model/margo.linkml.yaml" \
  >"${TGT_FILE}"
