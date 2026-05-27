#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
BUILD_DIR="${ROOT_DIR}/build"
BUILD_DOCS="${BUILD_DIR}/docs"

# Clean and create build directory
rm -rf "${BUILD_DOCS}"
mkdir -p "${BUILD_DOCS}"

# ─────────────────────────────────────────────────────────────────────────────
# Generate all artifacts
# Everything originates from spec/templates/ and flows through the pipeline
# ─────────────────────────────────────────────────────────────────────────────
"${ROOT_DIR}/tools/generate-class-diagram.bash"
"${ROOT_DIR}/tools/generate-json-schema.bash"
"${ROOT_DIR}/tools/generate-class-pages.bash"
"${ROOT_DIR}/tools/generate-spec-pages.bash"
"${ROOT_DIR}/tools/generate-openapi.bash"

# ─────────────────────────────────────────────────────────────────────────────
# Publish spec pages → build/docs/specification/
# Source of truth: spec/templates/spec-pages/ → spec/generated/spec-pages/
# ─────────────────────────────────────────────────────────────────────────────
mkdir -p "${BUILD_DOCS}/specification"
cp "${ROOT_DIR}/spec/generated/spec-pages/"*.md \
   "${BUILD_DOCS}/specification/" 2>/dev/null || true

# ─────────────────────────────────────────────────────────────────────────────
# Publish class pages → build/docs/data-models/
# Source of truth: spec/templates/class-pages/ → spec/generated/class-pages/
# ─────────────────────────────────────────────────────────────────────────────
mkdir -p "${BUILD_DOCS}/data-models"
mkdir -p "${BUILD_DOCS}/data-models/all"

cp "${ROOT_DIR}/spec/generated/class-pages/"*.md \
   "${BUILD_DOCS}/data-models/" 2>/dev/null || true

cp "${ROOT_DIR}/spec/generated/class-pages/all-data-models/"* \
   "${BUILD_DOCS}/data-models/all/" 2>/dev/null || true

# ─────────────────────────────────────────────────────────────────────────────
# Publish diagrams → build/docs/figures/
# ─────────────────────────────────────────────────────────────────────────────
mkdir -p "${BUILD_DOCS}/figures"
cp "${ROOT_DIR}/spec/generated/class-diagrams/"*.svg \
   "${BUILD_DOCS}/figures/" 2>/dev/null || true

# ─────────────────────────────────────────────────────────────────────────────
# Publish OpenAPI → build/docs/specification/margo-management-interface/
# ─────────────────────────────────────────────────────────────────────────────
mkdir -p "${BUILD_DOCS}/specification/margo-management-interface"
cp "${ROOT_DIR}/spec/generated/openapi/"*.yaml \
   "${BUILD_DOCS}/specification/margo-management-interface/" 2>/dev/null || true

# ─────────────────────────────────────────────────────────────────────────────
# Publish JSON schemas → build/docs/json-schemas/
# ─────────────────────────────────────────────────────────────────────────────
mkdir -p "${BUILD_DOCS}/json-schemas"
cp "${ROOT_DIR}/spec/generated/json-schemas/"*.json \
   "${BUILD_DOCS}/json-schemas/" 2>/dev/null || true

echo "✓ Build complete: ${BUILD_DOCS}"