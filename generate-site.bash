#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
BUILD_DIR="${ROOT_DIR}/build"
mkdir -p "${BUILD_DIR}"

# Copy static system-design docs into the build directory
cp -RH "${ROOT_DIR}/static/system-design/"* "${BUILD_DIR}/docs/system-design"

# Generate artifacts from source
"${ROOT_DIR}/spec/tools/generate-class-diagram.bash"
"${ROOT_DIR}/spec/tools/generate-json-schema.bash"
"${ROOT_DIR}/spec/tools/generate-docs.bash"
"${ROOT_DIR}/spec/tools/generate-openapi.bash"

# Move the generated docs into the build directory
mkdir -p "${BUILD_DIR}/data-model"
cp -R "${ROOT_DIR}/spec/generated/markdown/"* \
      "${BUILD_DIR}/data-model/"

# Publish diagrams
mkdir -p "${BUILD_DIR}/figures"
cp "${ROOT_DIR}/spec/generated/diagrams/"*.svg \
   "${BUILD_DIR}/figures/"

# Publish OpenAPI
MGMT="${BUILD_DIR}/specification/margo-management-interface"
mkdir -p "$MGMT"

cp "${ROOT_DIR}/spec/generated/openapi/"*.yaml \
   "$MGMT/"

# Publish JSON schemas
mkdir -p "${BUILD_DIR}/json-schemas"

cp "${ROOT_DIR}/spec/generated/json-schemas/"*.json \
   "${BUILD_DIR}/json-schemas/"