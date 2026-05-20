#!/usr/bin/env bash
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
TGT_DIR="${ROOT_DIR}/spec/generated/json-schemas"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  command -v linkml &>/dev/null || { echo "Missing: linkml"; exit 1; }
  RUN=""
fi

mkdir -p "$TGT_DIR"

# Schemas split across application/ and device/ subdirs
$RUN linkml generate json-schema \
  "${ROOT_DIR}/spec/data-model/application/deployment.linkml.yaml" > "${TGT_DIR}/application-deployment.schema.json"
$RUN linkml generate json-schema \
  "${ROOT_DIR}/spec/data-model/application/description.linkml.yaml" > "${TGT_DIR}/application-description.schema.json"
$RUN linkml generate json-schema \
  "${ROOT_DIR}/spec/data-model/device/deployment-status.linkml.yaml" > "${TGT_DIR}/deployment-status.schema.json"
$RUN linkml generate json-schema \
  "${ROOT_DIR}/spec/data-model/device/desired-state-manifest.linkml.yaml" > "${TGT_DIR}/desired-state-manifest.schema.json"
$RUN linkml generate json-schema \
  "${ROOT_DIR}/spec/data-model/device/capabilities.linkml.yaml" > "${TGT_DIR}/device-capabilities.schema.json"
