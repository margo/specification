#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"
DOCS_GEN="${THIS_DIR}"
CONFIGS="${DOCS_GEN}/configurations"

ROOT_DIR="$(dirname "$(dirname "${THIS_DIR}")")"

VERBOSITY="${1:-info}"

debug() {
    if [[ "$VERBOSITY" == "debug" ]] ; then
        echo "$1"
    fi
}

trace() {
    if [[ "$VERBOSITY" == "debug" ]] ||
       [[ "$VERBOSITY" == "trace" ]] ; then
        echo "$1"
    fi
}

info() {
    if [[ "$VERBOSITY" == "debug" ]] ||
       [[ "$VERBOSITY" == "trace" ]] ||
       [[ "$VERBOSITY" == "info" ]] ; then
        echo "$1"
    fi
}

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
    trace "********************************"
    SPEC_ROOT="${ROOT_DIR}/$(jq -r '.root' "${CONFIGS}/$1")"
    trace "Spec root folder: ${SPEC_ROOT}"

    TARGET_CLASS="$(jq -r '.targetclass' "${CONFIGS}/$1")"
    info "Target class: ${TARGET_CLASS}"

    SCHEMA_FILE="$(jq -r '.schemafile' "${CONFIGS}/$1")"
    trace "Schema file: ${SCHEMA_FILE}"

    EXAMPLES_DIR="${SPEC_ROOT}/resources/examples/valid"
    trace "Examples folder: ${EXAMPLES_DIR}"
    for EXAMPLE in $(ls "${EXAMPLES_DIR}"/${TARGET_CLASS}-0*.{yaml,json} 2>/dev/null) ; do
        if result=$(${RUN} linkml validate \
                --schema "${SPEC_ROOT}/${SCHEMA_FILE}" \
                --target-class "${TARGET_CLASS}" \
                "${EXAMPLE}") && \
                [[ "${result}" == "No issues found" ]] ; then
            echo "✅ Valid example (${EXAMPLE})"
        else
            echo "🚨 Not valid example expected to be valid! (${EXAMPLE})"
            echo "  ERROR: $result"
            exit 1
        fi
    done

    COUNTEREXAMPLES_DIR="${SPEC_ROOT}/resources/examples/invalid"
    for COUNTEREXAMPLE in $(ls "${COUNTEREXAMPLES_DIR}"/${TARGET_CLASS}-0*.{yaml,json} 2>/dev/null) ; do
        if ! result=$(${RUN} linkml validate \
                --schema "${SPEC_ROOT}/${SCHEMA_FILE}" \
                --target-class "${TARGET_CLASS}" \
                "${COUNTEREXAMPLE}") ; then
            echo "✅ Validation of invalid example failed, as expected (${COUNTEREXAMPLE})"
            debug "${result}"
        else
            echo "🚨 Validation of invalid example '${COUNTEREXAMPLE}' was expected to fail, but has succeeded."
            echo "${result}"
            exit 1
        fi
    done

    if false ; then
    # does not work due to following LinkML bugs:
    # https://github.com/linkml/linkml/issues/2423
    # https://github.com/linkml/linkml/issues/2425
    ${RUN} linkml examples \
        --schema "${SPEC_ROOT}/application-description.linkml.yaml" \
        --input-directory "${SPEC_ROOT}/resources/examples/valid" \
        --counter-example-input-directory "${SPEC_ROOT}/resources/examples/invalid" \
        --output-directory "${SPEC_ROOT}/output"
    fi
}

for spec in $(ls "${CONFIGS}") ; do
    check_spec "${spec}"
done

