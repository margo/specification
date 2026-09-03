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

check_spec () {
    SPEC_ROOT="${ROOT_DIR}/$(jq -r '.root' "${CONFIGS}/$1")"
    echo "Spec root folder: ${SPEC_ROOT}"

    TARGET_CLASS="$(jq -r '.targetclass' "${CONFIGS}/$1")"
    echo "Target class: ${TARGET_CLASS}"

    SCHEMA_FILE="$(jq -r '.schemafile' "${CONFIGS}/$1")"
    echo "Schema file: ${SCHEMA_FILE}"

    EXAMPLES_DIR="${SPEC_ROOT}/resources/examples/valid"
    echo "Examples folder: ${EXAMPLES_DIR}"
    for EXAMPLE in $(ls "${EXAMPLES_DIR}"/*-0*.yaml) ; do
        echo "Validate example: ${EXAMPLE}"
         ${RUN} linkml validate \
            --schema "${SPEC_ROOT}/${SCHEMA_FILE}" \
            --target-class "${TARGET_CLASS}" \
            "${EXAMPLE}"
    done

    COUNTEREXAMPLES_DIR="${SPEC_ROOT}/resources/examples/invalid"
    for COUNTEREXAMPLE in $(ls "${COUNTEREXAMPLES_DIR}"/*-0*.yaml) ; do
        if ! ${RUN} linkml validate \
                --schema "${SPEC_ROOT}/${SCHEMA_FILE}" \
                --target-class "${TARGET_CLASS}" \
                "${COUNTEREXAMPLE}" ; then
            echo "ok: validation failed, as expected"
        else
            echo "ERROR: Validation of 'examples/invalid/${COUNTEREXAMPLE}' was expected to fail, but has succeeded."
            exit 1
        fi
    done

    # does not work due to following LinkML bugs:
    # https://github.com/linkml/linkml/issues/2423
    # https://github.com/linkml/linkml/issues/2425
    if false ; then
    ${RUN} linkml examples \
        --schema "${SPEC_ROOT}/*.linkml.yaml" \
        --input-directory "${SPEC_ROOT}/resources/examples/valid" \
        --counter-example-input-directory "${SPEC_ROOT}/resources/examples/invalid" \
        --output-directory "${SPEC_ROOT}/output"
    fi
}

for spec in $(ls "${CONFIGS}") ; do
    check_spec "${spec}"
done

