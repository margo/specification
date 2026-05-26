```markdown
# linkml-to-openapi

A CLI tool that generates valid OpenAPI 3.0.x schemas from [LinkML](https://linkml.io/)
source files and injects them into an OpenAPI template.

Each schema stub in the template declares its own LinkML source via
`x-linkml-schema` and `x-linkml-source` extension fields. The tool resolves,
converts, and injects all schemas — including transitive dependencies — in a
single pass.

---

## How It Works

1. Reads an OpenAPI template YAML containing schema stubs with `x-linkml-*` fields
2. For each stub, runs LinkML's JSON Schema generator against the referenced file
3. Converts the output to OpenAPI 3.0.x (rewrites `$ref`s, normalises nullable
   patterns, wraps `$ref` siblings in `allOf`, strips `const`, etc.)
4. Injects the converted schema in-place, preserving any hand-authored fields
5. Auto-injects all transitive schema dependencies
6. Writes the fully resolved OpenAPI document to the output path

---

## Installation

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install the tool with dev dependencies
pip install -e ".[dev]"
```

---

## Usage

### Inject schemas into a template

```bash
linkml-to-openapi <template.yaml> <output.yaml>
```

```bash
# Example
linkml-to-openapi \
  ../spec/resources/openapi-templates/workload-management-api.template.yaml \
  ../spec/openapi/workload-management-api.generated.yaml
```

### With debug logging

```bash
linkml-to-openapi -v \
  ../../spec/resources/openapi-templates/workload-management-api.template.yaml \
  ../../spec/openapi/workload-management-api.generated.yaml
```

### List available definitions in a LinkML file

Useful for finding the correct `x-linkml-source` value when authoring stubs.
Does **not** require `template` or `output` arguments.

```bash
linkml-to-openapi --list-definitions path/to/schema.yaml
```

---

## Template Stub Format

Schema stubs in the OpenAPI template use two extension fields:

| Field              | Description                                              |
|--------------------|----------------------------------------------------------|
| `x-linkml-schema`  | Path to the LinkML file, relative to the template        |
| `x-linkml-source`  | Class or enum name to extract from that file             |

Any other fields on the stub (e.g. `description`, `example`) are preserved
in the output and take priority over the generated schema on conflict.

```yaml
# template.yaml
components:
  schemas:
    MyClass:
      x-linkml-schema: ../linkml/my-schema.yaml
      x-linkml-source: MyClass
      description: Optional hand-authored override description.
```

Schemas without both `x-linkml-schema` and `x-linkml-source` are left
untouched and passed through as-is.

---

## OpenAPI 3.0.x Conversions Applied

The following transformations are applied automatically during conversion:

| JSON Schema / LinkML pattern | OpenAPI 3.0.x output |
|------------------------------|----------------------|
| `$ref` with sibling keywords | `allOf: [{$ref: ...}]` + siblings |
| `type: [X, 'null']` | `type: X` + `nullable: true` |
| `anyOf: [{$ref: ...}, {type: null}]` | `allOf: [{$ref: ...}]` + `nullable: true` |
| `anyOf: [{schema}, {type: null}]` | schema inlined + `nullable: true` |
| `const: value` | stripped (captured by `enum: [value]`) |
| `#/$defs/X` references | `#/components/schemas/X` |

---

## Development

### Running tests

```bash
# All tests
pytest tests/

# With coverage report
pytest --cov=src tests/

# Specific test files
pytest tests/test_converter.py -v
pytest tests/test_injector.py -v
```

### Project structure

```
linkml-to-openapi/
├── src/
│   ├── converter.py   # JSON Schema → OpenAPI 3.0.x conversion logic
│   ├── injector.py    # Template walking and schema injection
│   └── cli.py         # CLI entry point and argument parsing
├── tests/
│   ├── test_converter.py
│   └── test_injector.py
├── pyproject.toml
└── README.md
```

---

## Requirements

- Python 3.10+
- `[LinkML](https://linkml.io/)` (`linkml` package)
- `[PyYAML](https://pyyaml.org/)`
` ` `