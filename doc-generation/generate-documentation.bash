#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"
ROOT_DIR="$(dirname "${THIS_DIR}")"
DOCS_GEN="${THIS_DIR}"
CONFIGS="${DOCS_GEN}/configurations"

if command -v poetry 2>&1 >/dev/null ; then
    RUN="poetry run"
else
    if ! command -v linkml 2>&1 >/dev/null ; then
        echo "The command 'linkml' is missing"
        exit 1
    fi
    if ! command -v mkdocs 2>&1 >/dev/null ; then
        echo "The command 'mkdocs' is missing"
        exit 1
    fi
    RUN=""
fi

gen_spec () {
    ITEM_REL_PATH=$(jq -r '.root' "${CONFIGS}/$1")
    SCHEMA_FILE=$(jq -r '.schemafile' "${CONFIGS}/$1")
    MKDOWN_FILE=$(jq -r '.markdowndoc' "${CONFIGS}/$1")
    SRC_ROOT="${ROOT_DIR}/${ITEM_REL_PATH}"
    SPEC_ROOT="${ROOT_DIR}/system-design${ITEM_REL_PATH#src}"
    echo "${SRC_ROOT}"

    ${RUN} linkml generate doc \
        --directory="${SRC_ROOT}/docs" \
        --template-directory="${SRC_ROOT}/resources" \
        "${SRC_ROOT}/${SCHEMA_FILE}"

    mv "${SRC_ROOT}/docs/index.md" "${SPEC_ROOT}/${MKDOWN_FILE}"
    rm -r "${SRC_ROOT}/docs"
}

for spec in $(ls "${CONFIGS}") ; do
    gen_spec "${spec}"
done

(
    cd "${ROOT_DIR}"
    ${RUN} mkdocs serve
)
