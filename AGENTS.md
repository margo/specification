# AGENTS.md — Margo Specification Contributor Guide

## Project Overview

The Margo Specification defines open standards for workload fleet management on edge compute devices. This repository contains the normative specification documents, some authored manually in MarkDown and others generated from a [LinkML](https://linkml.io/) data model using Jinja2 templates.

The final HTML documentation is built with [MkDocs](https://www.mkdocs.org/) using the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Repository Layout

```
.
├── model/                                # Aggregate data model (current source of truth)
│   ├── margo-data-model.linkml.yaml      # Top-level schema aggregating all sub-schemas
│   ├── application-description.linkml.yaml
│   ├── application-deployment.linkml.yaml
│   ├── desired-state-manifest.linkml.yaml
│   ├── device-capabilities.linkml.yaml
│   ├── deployment-status.linkml.yaml
│   ├── margo-resources.linkml.yaml
│   ├── margo-deployments.linkml.yaml
│   ├── generation-gap.md                 # Differences between pre-draft and generated OpenAPI spec
│   ├── examples/{valid,invalid}/         # Valid and invalid example files
│   └── diagrams/                         # Static PNG diagrams
├── system-design/                        # Tracked specification content (generated + manually-authored)
│   └── specification/margo-management-interface/
│       ├── specification-extensions.md   # Manually-authored extensions
│       └── workload-management-api-1.0.0.yaml  # Generated OpenAPI spec
├── tools/                                # Generation & validation scripts
│   ├── generate-all.bash                 # Runs all generators in sequence
│   ├── generate-docs.bash                # Generates MarkDown from LinkML, copies system-design/ → build/site/
│   ├── generate-json-schemas.bash        # Generates JSON-Schema artifacts
│   ├── generate-openapi.bash             # Generates OpenAPI spec (to build/artifacts/ + system-design/)
│   ├── generate-class-diagram.bash       # Generates PlantUML class diagrams
│   ├── check-examples.bash               # Validates schemas and examples
│   ├── openapigen.py                     # Custom OpenAPI generator
│   ├── configurations/                   # Per-spec JSON configs
│   │   ├── application-deployment.json
│   │   ├── application-description.json
│   │   ├── deployment-status.json
│   │   ├── desired-state-manifest.json
│   │   └── device-capabilities.json
│   └── templates/
│       ├── model/                        # Templates for the aggregate data-model docs
│       ├── main-classes/                 # Templates for per-resource docs
│       └── openapi/
│           └── workload-management-api-1.0.0.openapi.yaml   # OpenAPI template
├── docs/                                 # Manually-authored MarkDown (copied into build/site/ by generate-docs.bash)
│   ├── index.md
│   ├── CNAME
│   ├── assets/
│   ├── css/
│   └── specification/
│       ├── margo-management-interface/   # Manually-authored pages (api-requirements, certificate-api, etc.)
│       ├── applications/                 # application-registry.md (manually-authored)
│       ├── margo-devices/                # device-requirements.md
│       └── observability/                # 3 pages (publishing/collecting/consuming)
├── build/                                # Generated artifacts (tracked in git)
│   ├── artifacts/                        # diagrams, OpenAPI, JSON-Schema, intermediate markdown
│   │   ├── diagrams/
│   │   ├── json-schemas/
│   │   ├── main-classes/                 # Generated per-resource .md (intermediate)
│   │   ├── markdown/                     # Generated aggregate data-model .md (intermediate)
│   │   └── openapi/                      # Generated OpenAPI spec
│   └── site/                             # Merged MarkDown tree used by mkdocs build
├── CONTRIBUTING.md                       # Contribution requirements and process
├── legacy/                               # Archived superseded trees
│   ├── doc-generation/                   # Legacy scripts (superseded by tools/)
│   ├── src-specification/                # Legacy per-resource schemas + templates + examples
│   └── validate-openapi.py               # One-shot migration aid: compares generated spec vs pre-draft branch
├── mkdocs.yml                            # MkDocs configuration
└── pyproject.toml                        # Python dependencies (linkml@git, mkdocs, mkdocs-material, openapi-spec-validator)
```

## Setup

### Option A: Development Container

The repository includes a dev-container with all dependencies pre-installed. Open the repo in VS Code and accept the dev-container prompt.

### Option B: Poetry (recommended for local development)

```bash
poetry install
```

### Option C: pip

```bash
pip install -e .
```

## Key Commands

### Validate LinkML schemas and examples

```bash
tools/check-examples.bash
```

This script:
- Reads each config from `tools/configurations/*.json`
- Validates the corresponding LinkML schema
- Validates valid examples in `model/examples/valid/` against the schema
- Validates that invalid examples in `model/examples/invalid/` are correctly rejected
- Exits non-zero if any check fails

### Generate all artifacts

```bash
tools/generate-all.bash
```

This runs all generators in sequence: class diagrams, JSON-Schemas, OpenAPI, and MarkDown docs.

### Generate MarkDown from LinkML

```bash
tools/generate-docs.bash
```

This script:
- Generates per-resource MarkDown using `tools/templates/main-classes/`
- Generates the full data model MarkDown using `tools/templates/model/`
- Copies generated diagrams and OpenAPI spec into the merged tree
- Copies everything from `docs/` and `system-design/` into `build/site/` (which is what `mkdocs build` reads)

### Generate JSON-Schemas

```bash
tools/generate-json-schemas.bash
```

Generates one `.schema.json` file per resource schema into `build/artifacts/json-schemas/`.

### Generate OpenAPI spec

```bash
tools/generate-openapi.bash
```

Generates `workload-management-api-1.0.0.openapi.yaml` into `build/artifacts/openapi/`.

### Generate class diagrams

```bash
tools/generate-class-diagram.bash
```

Generates SVG/PNG class diagrams via PlantUML into `build/artifacts/diagrams/`.

### Build HTML documentation

```bash
mkdocs build          # one-time build
mkdocs serve          # live-reloading local server
```

## Generation Pipeline

Understanding how artifacts flow through the pipeline is essential when modifying schemas or templates.

### Artifact flow

```
model/*.linkml.yaml          (source of truth — LinkML schemas)
         │
         ├──► tools/check-examples.bash
         │       uses: tools/configurations/*.json
         │       validates: model/examples/{valid,invalid}/
         │
         ├──► tools/generate-docs.bash   (orchestrator)
         │       │
         │       ├──► linkml generate doc  (per-resource, using templates/main-classes/)
         │       │       → build/artifacts/main-classes/<schema>.md
         │       │       → moved into build/site/specification/{applications,margo-management-interface}/
         │       │
         │       ├──► linkml generate doc  (aggregate, using templates/model/)
         │       │       → build/artifacts/markdown/*
         │       │       → moved into build/site/data-model/
         │       │
         │       ├──► generate-class-diagram.bash
         │       │       → build/artifacts/diagrams/DataModel-ClassDiagram.{svg,png}
         │       │       → copied into build/site/figures/
         │       │
         │       ├──► generate-openapi.bash
         │       │       → build/artifacts/openapi/workload-management-api-1.0.0.openapi.yaml
         │       │       → moved into build/site/specification/margo-management-interface/
         │       │       → also written to system-design/specification/margo-management-interface/ (tracked)
         │       │
         │       └──► JSON schemas copied into build/site/json-schemas/
         │
         └──► tools/generate-json-schemas.bash   (standalone)
                 → build/artifacts/json-schemas/*.schema.json

mkdocs build  reads from build/site/   →   site/
```

Key points:
- `mkdocs build` reads from `build/site/`, not directly from `docs/` or `build/artifacts/`. The `generate-docs.bash` script copies everything into `build/site/` first.
- The per-resource Markdown generation and the aggregate data-model generation use **different template directories** and produce output in **different locations**.
- `check-examples.bash` reads the list of schemas from `tools/configurations/*.json`, but `generate-docs.bash` and `generate-json-schemas.bash` have **hardcoded** schema lists. When adding a new resource, you must update all three.

### OpenAPI generation

The OpenAPI spec is generated by `tools/openapigen.py`, which:
- Reads an OpenAPI template (`tools/templates/openapi/workload-management-api-1.0.0.openapi.yaml`) that defines endpoints, security schemes, and request/response structure.
- Fills in `components/schemas` from the LinkML model using the JSON-Schema generator.
- Only classes referenced by the endpoints in the template are included in the output.

When adding a new resource to the API, you must update both the LinkML schema **and** the OpenAPI template (add new endpoints that reference the new class). The template follows standard OpenAPI 3.0.3 structure — add a new entry under `paths` with request/response schemas that use `$ref: "#/components/schemas/<ClassName>"`.

## Legacy Code

The `legacy/src-specification/` directory contains the original per-resource LinkML schemas, templates, and examples. These are **legacy** and no longer the source of truth. The current source of truth is `model/`. Do not modify files under `legacy/src-specification/` unless specifically instructed.

The `legacy/doc-generation/` directory contains the original generation and validation scripts. These have been superseded by `tools/`. Do not use the old scripts.

The `legacy/validate-openapi.py` script is a one-shot migration aid that compares the generated OpenAPI spec against the hand-written spec on the `pre-draft` branch. See `legacy/README.md` for usage details. It becomes obsolete once `pre-draft` is fully replaced by the generated spec, at which point it should be deleted.

## How to Modify the LinkML Data Model

### Step 1: Edit the schema

The **source of truth** for LinkML-specified resources lives under `model/`. Each resource has its own `.linkml.yaml` file. The aggregate schema `model/margo-data-model.linkml.yaml` imports all sub-schemas.

When making changes:

1. Edit the relevant `.linkml.yaml` file to add/modify classes, attributes, enums, slots, or types.
2. Add or update valid examples in `model/examples/valid/` to cover the new or changed model elements.
3. Add invalid counter-examples in `model/examples/invalid/` if new validation rules are introduced.
4. If the change affects rendering, update the Jinja2 templates:
   - `tools/templates/main-classes/` — for per-resource specification pages (attribute tables, examples, JSON-Schema links).
   - `tools/templates/model/` — for the aggregate data-model documentation (class hierarchy, diagrams).
5. If the change adds new API endpoints, update the OpenAPI template `tools/templates/openapi/workload-management-api-1.0.0.openapi.yaml`.

### Step 2: Validate

```bash
tools/check-examples.bash
```

Fix any validation errors before proceeding.

### Step 3: Regenerate artifacts

```bash
tools/generate-all.bash
```

This runs all generators in sequence. Alternatively, run individual generators if you only need to update one artifact type.

The generated `.md` files land under `docs/specification/` and `docs/data-model/`. Generated JSON-Schemas, OpenAPI specs, and diagrams land under `build/artifacts/`. Verify the output looks correct.

### Step 4: Preview the site

```bash
mkdocs serve
```

Open http://127.0.0.1:8000 and navigate to the relevant specification page to visually verify.

### Step 5: Commit

Include the modified LinkML schema, updated examples, and all regenerated artifacts (`docs/`, `build/`) in your commit. These directories are tracked in git and must reflect the generated output.

## Adding a New LinkML-Specified Resource

1. Add the LinkML schema: `model/<resource-name>.linkml.yaml`.
2. Add valid examples: `model/examples/valid/<TargetClass>-NNN.{yaml,json}`.
3. Add invalid counter-examples: `model/examples/invalid/<TargetClass>-NNN.{yaml,json}`.
4. Add a configuration file in `tools/configurations/<resource-name>.json` with:
   ```json
   {
       "root": "model",
       "targetclass": "<RootClassName>",
       "schemafile": "<resource-name>.linkml.yaml",
       "markdowndoc": "<output-filename>.md"
   }
   ```
5. Add an import in `model/margo-data-model.linkml.yaml`.
6. Add the new MarkDown file to `mkdocs.yml` under the `nav` section.
7. Add the schema name to the hardcoded lists in `generate-docs.bash` (line 41) and `generate-json-schemas.bash` (line 24).
8. Run validation and generation as described above.

## Jinja2 Templates

The generation uses `linkml generate doc`, which provides the following variables and objects in the template context:

- `schema` — the parsed LinkML schema object
- `schemaview` — a `SchemaView` instance for querying classes, slots, enums, etc.
- `gen` — the generator instance with helper methods like `all_class_objects()`, `get_direct_slots()`, `link()`, `mermaid_diagram()`

Common patterns in existing templates:

- Iterate over class slots: `{% for slot in schemaview.class_slots("ClassName")|sort(attribute='rank') %}`
- Get slot details: `schemaview.get_slot(slot_name).range`, `.required`, `.description`
- Include example files: `{% include 'examples/valid/FileName.yaml' %}`
- Format ranges with inline macros for multivalued/inlined slots (see `index.md.jinja2` in each template directory)

There are two separate sets of templates that serve different purposes:

| Template directory | Used by | Produces | Output location |
| --- | --- | --- | --- |
| `tools/templates/main-classes/` | `generate-docs.bash` (per-resource loop) | One `.md` per schema with attribute tables, examples, JSON-Schema links | `build/site/specification/{applications,margo-management-interface}/` |
| `tools/templates/model/` | `generate-docs.bash` (aggregate step) | Full data model overview with class hierarchy, diagrams, all-class listing | `build/site/data-model/` |

Each directory contains an `index.md.jinja2` (the main page) and may contain `class.md.jinja2` (individual class detail pages). When modifying rendering, determine which template directory to edit based on the table above.

**When do templates need updating?** Most schema changes (adding/removing attributes, changing types, adding enums) do **not** require template changes — the templates iterate dynamically over class slots. Templates need updating only when:
- Changing the **structure** of the rendered page (e.g., adding a new section, changing table columns)
- Changing how **multivalued/inlined ranges** are displayed (the `format_range` macro in `index.md.jinja2`)
- Adding support for a **new example format** (e.g., rendering `.json` examples alongside `.yaml`)

## CI

The GitHub Actions pipeline (`.github/workflows/pages.yml`) runs:

1. **Quality checks** — validates `pyproject.toml` and `poetry.lock` consistency
2. **Validation** — runs `tools/check-examples.bash`
3. **Document generation** — runs `tools/generate-docs.bash`
4. **Pages build & deploy** — deploys to GitHub Pages on the `pre-draft` branch

PR checks (`.github/workflows/pr-checks.yml`) verify that commits are signed off.

## Conventions

- Sign off all commits (`git commit -s`)
- All contributions require CLA compliance (EasyCLA)
- One logical change per commit; the tree must build and work after each commit
- Base PRs on the `pre-draft` branch
- Example files follow the naming convention `<TargetClass>-NNN.{yaml,json}` (e.g., `ApplicationDescription-001.yaml`, `DeploymentStatusManifest-001.json`)
- LinkML schemas use the `.linkml.yaml` extension
- The YAML language server schema annotation `# yaml-language-server: $schema=...` should be kept at the top of each schema file for IDE support
- Do **not** add `default_range: string` to schemas that define slots using `any_of` — it causes the JSON-Schema generator to emit `type: string` at the top level, overriding the `anyOf` union. See [linkml/linkml#1483](https://github.com/linkml/linkml/issues/1483)
- Omit explicit `required: false` on optional attributes — the LinkML default is already `false`
