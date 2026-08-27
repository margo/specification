#!/usr/bin/env bash

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"
ROOT_DIR="$(dirname "${THIS_DIR}")"
DOCS_GEN="${THIS_DIR}"
SPEC_DIR="${SPEC_DIR:-${ROOT_DIR}/system-design/specification}"

if command -v poetry >/dev/null 2>&1 ; then
    RUN="poetry run"
else
    if ! python3 -c 'import openapi_spec_validator' >/dev/null 2>&1 ; then
        echo "The Python module 'openapi_spec_validator' is missing"
        exit 1
    fi
    RUN=""
fi

echo "Specification folder: ${SPEC_DIR}"

DOCUMENTS=()
while IFS= read -r DOCUMENT ; do
    echo "OpenAPI document: ${DOCUMENT}"
    DOCUMENTS+=("${DOCUMENT}")
done < <(find "${SPEC_DIR}" -type f \
             \( -name '*-api-*.yaml' -o -name '*-api-*.yml' \) | sort)

# A document with a damaged first line has no readable 'openapi' key. Discovery
# by file name therefore finds it, and discovery by content does not.
if [ "${#DOCUMENTS[@]}" -eq 0 ] ; then
    echo "ERROR: no OpenAPI document was found under '${SPEC_DIR}'."
    echo "ERROR: check the name pattern in this script."
    exit 1
fi

${RUN} python3 "${DOCS_GEN}/check_openapi.py" "${DOCUMENTS[@]}"
