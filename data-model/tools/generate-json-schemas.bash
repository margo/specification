#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

TGT_DIR="${ROOT_DIR}/generated/json-schemas"

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

for schema in "application-deployment" "application-description" "deployment-status" "desired-state-manifest" "device-capabilities"; do
  ${RUN} linkml generate json-schema "${ROOT_DIR}/data-model/${schema}.linkml.yaml" >"${TGT_DIR}/${schema}.schema.json"
done
