"""Validate the OpenAPI documents of the Margo specification."""

import sys

from openapi_spec_validator import (
    OpenAPIV30SpecValidator,
    OpenAPIV31SpecValidator,
    OpenAPIV32SpecValidator,
)
from openapi_spec_validator.readers import read_from_filename

VALIDATORS = {
    "3.0": OpenAPIV30SpecValidator,
    "3.1": OpenAPIV31SpecValidator,
    "3.2": OpenAPIV32SpecValidator,
}


def check_document(path):
    """Validate one document. Return True if the document is valid."""
    try:
        spec, base_uri = read_from_filename(path)
    except Exception as error:
        print(f"ERROR: {path}: the file is not readable: {error}")
        return False

    if not isinstance(spec, dict):
        print(f"ERROR: {path}: the document is not a YAML mapping.")
        return False

    declared = spec.get("openapi")
    if declared is None:
        # A damaged first line hides the key. Print the keys with ascii() so
        # that an invisible character becomes visible.
        keys = ", ".join(ascii(key) for key in spec)
        print(f"ERROR: {path}: the top-level 'openapi' version field is absent.")
        print(f"ERROR: {path}: the top-level keys are: {keys}")
        return False

    if not isinstance(declared, str):
        # An unquoted value such as "openapi: 3.1" parses as a number.
        print(f"ERROR: {path}: the 'openapi' version must be a string.")
        print(f"ERROR: {path}: the value {declared!r} is not a string.")
        return False

    version = declared[:3]
    if version not in VALIDATORS:
        supported = ", ".join(sorted(VALIDATORS))
        print(f"ERROR: {path}: the 'openapi' version {declared!r} is not supported.")
        print(f"ERROR: {path}: this check supports {supported}.")
        return False

    validator = VALIDATORS[version](spec, base_uri=base_uri)
    errors = list(validator.iter_errors())
    if not errors:
        print(f"ok: {path} is a valid OpenAPI {version} document")
        return True

    for error in errors:
        where = "/".join(str(part) for part in error.absolute_path)
        print(f"ERROR: {path}: {where or '(document root)'}: {error.message}")
    return False


def main(paths):
    if not paths:
        print("ERROR: no OpenAPI document was given")
        return 1
    results = [check_document(path) for path in paths]
    if all(results):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
