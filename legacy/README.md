# Legacy

This directory contains artifacts from the pre-migration era that should
disappear once this branch has been merged into `pre-draft`.

- `doc-generation/` — original generation scripts (superseded by `tools/`).
- `src-specification/` — original per-resource schemas and templates
  (superseded by `model/` and `tools/templates/`).
- `validate-openapi.py` — one-shot migration aid comparing the generated
  OpenAPI spec against the hand-written `pre-draft` branch.

## Usage: `validate-openapi.py`

Requires Poetry dependencies (`poetry install`). Run from repository root.

### Full comparison

```
poetry run python legacy/validate-openapi.py
```

Prints a structural diff between the generated OpenAPI spec and the `pre-draft`
branch: added/removed schemas, changed properties, type mismatches.

### Single schema detail

```
poetry run python legacy/validate-openapi.py --schema <SchemaName>
poetry run python legacy/validate-openapi.py -s <SchemaName>
```

> [!Tip]
> Example: `poetry run python legacy/validate-openapy.py --schema DeploymentBundleRef`

Shows verbose details for one schema only. `<SchemaName>` is the name as it
appears in the generated output's `components/schemas`.

### With YAML dump

```
poetry run python legacy/validate-openapi.py --schema <SchemaName> --yaml
poetry run python legacy/validate-openapi.py -s <SchemaName> -y
```

Prints the pre-draft and generated YAML for the given schema.

> [!Tip]
> Example: `poetry run python legacy/validate-openapy.py --schema DeploymentBundleRef --yaml`
