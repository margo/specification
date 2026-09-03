#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

echo "Generate Class Diagrams"
"${THIS_DIR}/generate-class-diagram.bash"
echo "Generate JSON Schemas"
"${THIS_DIR}/generate-json-schemas.bash"
echo "Generate OpenAPI specification"
"${THIS_DIR}/generate-openapi.bash"
echo "Generate Documentation"
"${THIS_DIR}/generate-docs.bash"
echo "Done"
