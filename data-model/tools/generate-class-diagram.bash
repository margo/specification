#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

TGT_DIR="${ROOT_DIR}/generated/diagrams"

mkdir -p "${TGT_DIR}"

linkml generate plantuml --directory "${TGT_DIR}" --format svg "${ROOT_DIR}/data-model/margo-data-model.linkml.yaml"
