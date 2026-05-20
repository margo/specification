#!/usr/bin/env bash
set -eu

# ── Paths ────────────────────────────────────────────────────────────────────
THIS_DIR="$(dirname "$(readlink -f "$0")")"
ROOT_DIR="$(git rev-parse --show-toplevel)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  for cmd in linkml mkdocs; do
    command -v "$cmd" &>/dev/null || { echo "Missing: $cmd"; exit 1; }
  done
  RUN=""
fi

DATA_MODEL="${ROOT_DIR}/spec/data-model"
TEMPLATES="${ROOT_DIR}/spec/resources/markdown-templates"
EXAMPLES="${ROOT_DIR}/spec/resources/examples/valid"
BUILD_DIR="${ROOT_DIR}/build"

# ── Setup build dir ──────────────────────────────────────────────────────────
mkdir -p "${BUILD_DIR}"
cp -RH "${ROOT_DIR}/static/system-design/"* "${BUILD_DIR}/"

# ── Main class docs ──────────────────────────────────────────────────────────
TGT_DIR="${ROOT_DIR}/spec/generated/markdown_main-classes"
mkdir -p "$TGT_DIR"

$RUN linkml generate doc --directory="$TMP_DIR" \
  --template-directory="${TEMPLATES}_main-classes" \
  --preserve-names \
  --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/application/description.linkml.yaml"
mv "$TMP_DIR/index.md" "${TGT_DIR}/description.md"

$RUN linkml generate doc --directory="$TMP_DIR" \
  --template-directory="${TEMPLATES}_main-classes" \
  --preserve-names \
  --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/application/deployment.linkml.yaml"
mv "$TMP_DIR/index.md" "${TGT_DIR}/deployment.md"

$RUN linkml generate doc --directory="$TMP_DIR" \
  --template-directory="${TEMPLATES}_main-classes" \
  --preserve-names \
  --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/device/deployment-status.linkml.yaml"
mv "$TMP_DIR/index.md" "${TGT_DIR}/deployment-status.md"

$RUN linkml generate doc --directory="$TMP_DIR" \
  --template-directory="${TEMPLATES}_main-classes" \
  --preserve-names \
  --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/device/desired-state-manifest.linkml.yaml"
mv "$TMP_DIR/index.md" "${TGT_DIR}/desired-state-manifest.md"

$RUN linkml generate doc --directory="$TMP_DIR" \
  --template-directory="${TEMPLATES}_main-classes" \
  --preserve-names \
  --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/device/capabilities.linkml.yaml"
mv "$TMP_DIR/index.md" "${TGT_DIR}/capabilities.md"
rm -rf "${TMP_DIR:?}/"*

MGMT="${BUILD_DIR}/specification/margo-management-interface"
mv "${TGT_DIR}/deployment-status.md"  "$MGMT/"
mv "${TGT_DIR}/device-capabilities.md" "$MGMT/"
mv "${TGT_DIR}/application-description.md" "${BUILD_DIR}/specification/applications/"

# ── Whole data model docs ────────────────────────────────────────────────────
TGT_DIR="${ROOT_DIR}/spec/generated/markdown"
mkdir -p "$TGT_DIR"

$RUN linkml generate doc \
  --directory="$TGT_DIR" \
  --template-directory="$TEMPLATES" \
  --preserve-names --stacktrace \
  --example-directory="$EXAMPLES" \
  "${DATA_MODEL}/margo.linkml.yaml"

mv "$TGT_DIR"/* "${BUILD_DIR}/data-model/"

# ── Diagrams ─────────────────────────────────────────────────────────────────
"${THIS_DIR}/generate-class-diagram.bash"
cp "${ROOT_DIR}/spec/generated/diagrams/DataModel-ClassDiagram".{svg,png} \
  "${BUILD_DIR}/figures/"

# ── OpenAPI ──────────────────────────────────────────────────────────────────
"${THIS_DIR}/generate-openapi.bash"
mv "${ROOT_DIR}/spec/generated/openapi/workload-management-api.openapi.template.yaml" \
   "${MGMT}/workload-management-api-1.0.0.yaml"

# ── JSON Schemas ─────────────────────────────────────────────────────────────
MERGED_JSON_DIR="${BUILD_DIR}/json-schemas"
mkdir -p "$MERGED_JSON_DIR"
for f in "${ROOT_DIR}/spec/generated/json-schemas/"*.schema.json; do
  [[ -f "$f" ]] && cp "$f" "$MERGED_JSON_DIR/"
done
