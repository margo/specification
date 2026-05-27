# DEV_GUIDE.md

# Developer Guide

This guide covers how the specification toolchain works, how to contribute
to the specification itself, and how to extend or modify the toolchain.

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [How It Works](#how-it-works)
3. [Contributing to the Specification](#contributing-to-the-specification)
4. [Contributing to the Toolchain](#contributing-to-the-toolchain)
5. [Impact Map](#impact-map)

---

## Repository Structure

```
spec/
├── data-models/       ← LinkML schemas — source of truth for all data structures
├── templates/
│   ├── class-pages/   ← Jinja2 templates defining how class docs look
│   ├── openapi/       ← OpenAPI stub templates
│   └── spec-pages/    ← human-authored specification pages which can be 
|                       templatized using html tags to inject class page content
├── examples/
│   ├── valid/         ← validated in CI against schemas
│   └── invalid/       ← validated in CI against schemas
└── generated/         ← pipeline output only — never edit, never commit

tools/
├── generate-class-pages.bash    ← LinkML + Jinja2 → class markdown files
├── generate-spec-pages.bash     ← spec-pages + class pages → final spec pages
├── generate-openapi.bash        ← OpenAPI template → resolved OpenAPI YAML
├── generate-class-diagram.bash  ← LinkML → SVG diagrams via Kroki
├── generate-json-schema.bash    ← LinkML → JSON Schema
├── check-examples.bash          ← validates examples against schemas
├── spec-page-assembler/         ← Python: injects class pages into spec pages
└── configurations/              ← config YAMLs driving each tool
```

---

## How It Works

All data structures are defined **once** in LinkML schemas (`spec/data-models/`).
Everything else — class documentation, OpenAPI, JSON Schema, diagrams — is
generated from those schemas by the pipeline. There is no duplication.

### Pipeline Order

```
spec/data-models/
        │
        ├──→ [1] generate-class-diagram.bash  →  spec/generated/class-diagrams/
        ├──→ [2] generate-json-schema.bash    →  spec/generated/json-schemas/
        ├──→ [3] generate-class-pages.bash    →  spec/generated/class-pages/
        │                │
        │    spec/templates/spec-pages/  ←── humans write here
        │                │
        ├──→ [4] generate-spec-pages.bash     →  spec/generated/spec-pages/
        └──→ [5] generate-openapi.bash        →  spec/generated/openapi/
```

`generate-site.bash` runs all steps in order and copies outputs to `build/docs/`
for mkdocs to serve.

### Why `spec/generated/` Is Gitignored

Generated files are derived artifacts — the same schema always produces the
same output. Committing them causes merge conflicts on every schema change,
pollutes PR diffs, and creates a second place to maintain. The pipeline
regenerates everything from source on every build.

### Inject Markers

Spec pages are human-authored but can embed generated class tables using:

```markdown
<!-- linkml:inject class="DeviceCapabilitiesManifest" -->
```

The `spec-page-assembler` resolves these at pipeline time by reading the
corresponding file from `spec/generated/class-pages/`. Authors never need
to know generated file paths, but ensure that the class name matches the LinkML
definition. Files with no markers pass through unchanged.

---

## Contributing to the Specification

### Editing an Existing Data Model

Edit the relevant file in `spec/data-models/`. The pipeline regenerates
all class pages, OpenAPI, JSON Schema, and diagrams automatically.

If you rename or remove a class, check for broken inject markers in
`spec/templates/spec-pages/`.

### Adding a New Data Model

**1.** Create `spec/data-models/your-model.linkml.yaml` and import it in
`margo.linkml.yaml`:

```yaml
imports:
  - your-model.linkml
```

**2.** Register it in the config files:

```yaml
# tools/configurations/markdown.config.yaml
- name: your-model
  doc_template_dir: spec/templates/class-pages/main-classes
  input:
    schema: spec/data-models/your-model.linkml.yaml
  output:
    md: spec/generated/class-pages/your-model.md

# tools/configurations/json-schema.config.yaml
- name: your-model
  input:
    schema: spec/data-models/your-model.linkml.yaml
  output:
    json_schema: spec/generated/json-schemas/your-model.schema.json

# tools/configurations/uml.config.yml
- name: YourModel-ClassDiagram
  schema: spec/data-models/your-model.linkml.yaml
  classes_to_render:
    - YourMainClass
  pipeline: []
  output:
    svg: spec/generated/class-diagrams/YourModel.svg

# tools/configurations/examples.config.yaml
- name: your-model
  schema: spec/data-models/your-model.linkml.yaml
  target_class: YourMainClass
  examples:
    valid: spec/examples/valid
    invalid: spec/examples/invalid
```

**3.** Add examples:

```
spec/examples/valid/YourMainClass-001.yaml
spec/examples/invalid/YourMainClass-001-missing-required.yaml
```

**4.** Create a spec page in `spec/templates/spec-pages/your-model.md`:

```markdown
# Your Model

Human-authored introduction and rationale...

## Attributes
<!-- linkml:inject class="YourMainClass" -->
```

**5.** Add to `mkdocs.yml`:

```yaml
- Specification:
    - Your Model: specification/your-model.md
- Data Models:
    - YourModel: data-models/your-model.md
```

**Checklist**
- [ ] Schema created and imported in `margo.linkml.yaml`
- [ ] Entry in `markdown.config.yaml`
- [ ] Entry in `json-schema.config.yaml`
- [ ] Entry in `uml.config.yml`
- [ ] Entry in `examples.config.yaml`
- [ ] Valid and invalid examples added
- [ ] Spec page created in `spec/templates/spec-pages/`
- [ ] Nav entries added to `mkdocs.yml`

### Editing a Spec Page

Edit the file directly in `spec/templates/spec-pages/`. Use inject markers
where you want generated class content. The pipeline picks up all changes
automatically — no config update needed.

### Adding Examples

Drop files into `spec/examples/valid/` or `spec/examples/invalid/` following
the naming convention `LinkMLClassName-NNN.yaml`. `check-examples.bash` picks them
up automatically based on the class name prefix.

---

## Contributing to the Toolchain

### Changing How Class Pages Look

Edit the Jinja2 templates in `spec/templates/class-pages/main-classes/` or
`spec/templates/class-pages/all-classes/`. Changes affect all class pages
rendered with that template, and all spec pages that inject those class pages.

To add a new template style, create a new directory under
`spec/templates/class-pages/` and reference it via `doc_template_dir` in
`markdown.config.yaml`.

### Adding a Diagram

Add an entry to `tools/configurations/uml.config.yml`:

```yaml
- name: YourModel-ClassDiagram
  schema: spec/data-models/your-model.linkml.yaml
  classes_to_render:
    - YourMainClass
  pipeline:
    - explicitly_add_uml_relationship: "ChildClass ..> ParentClass"
    - delete_uml_block: "UnwantedClass.*{$"
  output:
    svg: spec/generated/class-diagrams/YourModel.svg
```

Diagrams are rendered via `[Kroki](https://kroki.io)` — no local PlantUML needed.

### Adding a New Tool

1. Create `tools/generate-your-thing.bash` — follow the pattern of existing
   scripts: use `ROOT_DIR`, drive from a config YAML, write to `spec/generated/`
2. Create `tools/configurations/your-thing.config.yaml`
3. Add the script call to `generate-site.bash`
4. Add the copy step in `generate-site.bash` to publish output to `build/docs/`

### Modifying `spec-page-assembler`

`tools/spec-page-assembler/main.py` is the only Python tool written in this
repo. It reads inject markers and resolves them against `spec/generated/class-pages/`.
To add a new marker type, add a new `if` branch in the `replace()` function
following the existing `class` and `example` patterns.

---

## Impact Map

| What you change | What is affected |
|-----------------|-----------------|
| A class in `spec/data-models/` | Class pages, JSON Schema, OpenAPI, diagrams |
| Rename/remove a class | Above + inject markers in `spec/templates/spec-pages/` |
| An attribute or enum | Class pages, JSON Schema, OpenAPI |
| `types.linkml.yaml` | Every schema that imports it — all outputs |
| Add a new `.linkml.yaml` | Nothing automatically — must update all config files |
| Jinja2 template in `class-pages/` | All class pages using that template + spec pages that inject them |
| A file in `spec-pages/` | Only that spec page's output |
| Add a new spec page | Must also add to `mkdocs.yml` |
| `spec-page-assembler/main.py` | All spec page generation |
| Any `configurations/*.yaml` | Only the tool that reads that config |
| `generate-site.bash` | The entire build |
| `mkdocs.yml` | Site navigation only |