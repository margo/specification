#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

"${THIS_DIR}/generate-class-diagram.bash"
"${THIS_DIR}/generate-json-schemas.bash"
"${THIS_DIR}/generate-openapi.bash"
"${THIS_DIR}/generate-docs.bash"
