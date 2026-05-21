#!/usr/bin/env bash

set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
BUILD_DIR="${ROOT_DIR}/build"
BUILD_DOCS="${BUILD_DIR}/docs"

# Clean and create build directory
rm -rf "${BUILD_DOCS}"
mkdir -p "${BUILD_DOCS}"

# Create all necessary directories upfront
mkdir -p "${BUILD_DOCS}/system-design/specification/margo-management-interface"
mkdir -p "${BUILD_DOCS}/system-design/specification/applications"
mkdir -p "${BUILD_DOCS}/system-design/specification/margo-devices"
mkdir -p "${BUILD_DOCS}/system-design/specification/observability"
mkdir -p "${BUILD_DOCS}/system-design/concepts/applications"
mkdir -p "${BUILD_DOCS}/system-design/concepts/edge-compute-devices"
mkdir -p "${BUILD_DOCS}/system-design/concepts/workload-fleet-managers"
mkdir -p "${BUILD_DOCS}/system-design/overview"
mkdir -p "${BUILD_DOCS}/system-design/personas-and-definitions"
mkdir -p "${BUILD_DOCS}/system-design/figures"
mkdir -p "${BUILD_DOCS}/data-model"
mkdir -p "${BUILD_DOCS}/figures"
mkdir -p "${BUILD_DOCS}/json-schemas"
mkdir -p "${BUILD_DOCS}/make-a-contribution"

# Copy static system-design docs into the build directory
cp -RH "${ROOT_DIR}/static/system-design/specification"/* "${BUILD_DOCS}/system-design/specification/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/system-design/concepts"/* "${BUILD_DOCS}/system-design/concepts/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/system-design/overview"/* "${BUILD_DOCS}/system-design/overview/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/system-design/personas-and-definitions"/* "${BUILD_DOCS}/system-design/personas-and-definitions/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/system-design/make-a-contribution"/* "${BUILD_DOCS}/make-a-contribution/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/system-design/figures"/* "${BUILD_DOCS}/system-design/figures/" 2>/dev/null || true
cp -RH "${ROOT_DIR}/static/figures"/* "${BUILD_DOCS}/figures/" 2>/dev/null || true
cp "${ROOT_DIR}/static/system-design/index.md" "${BUILD_DOCS}/" 2>/dev/null || true

# Generate artifacts from source
"${ROOT_DIR}/spec/tools/generate-class-diagram.bash"
"${ROOT_DIR}/spec/tools/generate-json-schema.bash"
"${ROOT_DIR}/spec/tools/generate-docs.bash"
"${ROOT_DIR}/spec/tools/generate-openapi.bash"

# Copy generated data-model docs to root data-model/ directory (as expected by mkdocs.yml)
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/all-data-models/"* \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true

# Copy main class markdown files
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/application-description.md" \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/application-deployment.md" \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/deployment-status.md" \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/device-capabilities.md" \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true
cp "${ROOT_DIR}/spec/generated/markdown_main-classes/desired-state-manifest.md" \
   "${BUILD_DOCS}/data-model/" 2>/dev/null || true

# Publish diagrams to both locations
mkdir -p "${BUILD_DOCS}/figures"
cp "${ROOT_DIR}/spec/generated/diagrams/"*.svg "${BUILD_DOCS}/figures/" 2>/dev/null || true
cp "${ROOT_DIR}/spec/generated/diagrams/"*.svg "${BUILD_DOCS}/system-design/figures/" 2>/dev/null || true

# Publish OpenAPI
cp "${ROOT_DIR}/spec/generated/openapi/"*.yaml \
   "${BUILD_DOCS}/system-design/specification/margo-management-interface/" 2>/dev/null || true

# Publish JSON schemas
cp "${ROOT_DIR}/spec/generated/json-schemas/"*.json \
   "${BUILD_DOCS}/json-schemas/" 2>/dev/null || true

# Create data-model index if it doesn't exist
if [ ! -f "${BUILD_DOCS}/data-model/index.md" ]; then
  cat > "${BUILD_DOCS}/data-model/index.md" << 'EOF'
# Data Model Reference

This section contains the complete data model specifications for Margo, auto-generated from LinkML schemas.

## Main Classes

- [ApplicationDescription](application-description.md)
- [ApplicationDeployment](application-deployment.md)
- [Device Capabilities](device-capabilities.md)
- [Desired State Manifest](desired-state-manifest.md)
- [Deployment Status](deployment-status.md)

## Full Reference

See [All Data Models](all-data-models/index.md) for the complete reference of all classes, types, and definitions.
EOF
fi

echo "✓ Build complete: ${BUILD_DOCS}"