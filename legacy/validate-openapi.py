#!/usr/bin/env python3
"""Compare the pre-draft OpenAPI spec with the generated one at object level."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


# ── Color support ──────────────────────────────────────────────
_USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text


def bold(text: str) -> str:
    return _c("1", text)


def green(text: str) -> str:
    return _c("32", text)


def red(text: str) -> str:
    return _c("31", text)


def yellow(text: str) -> str:
    return _c("33", text)


def cyan(text: str) -> str:
    return _c("36", text)


def dim(text: str) -> str:
    return _c("2", text)


# ───────────────────────────────────────────────────────────────


ROOT = Path(__file__).resolve().parent.parent
PRE_DRAFT_FILE = "system-design/specification/margo-management-interface/workload-management-api-1.0.0-rc.2.yaml"
GENERATED_FILE = "system-design/specification/margo-management-interface/workload-management-api-1.0.0-rc.2.yaml"
# GENERATED_FILE = "build/artifacts/openapi/workload-management-api-1.0.0.openapi.yaml"


def get_pre_draft_spec() -> dict:
    """Retrieve the OpenAPI spec from the pre-draft branch."""
    result = subprocess.run(
        ["git", "show", f"pre-draft:{PRE_DRAFT_FILE}"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode == 0:
        return yaml.safe_load(result.stdout)
    print(f"ERROR: could not retrieve pre-draft file: {result.stderr}", file=sys.stderr)
    sys.exit(1)


def get_generated_spec() -> dict:
    """Read the generated OpenAPI spec from disk."""
    path = ROOT / GENERATED_FILE
    if not path.exists():
        print(f"ERROR: generated file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def deep_diff(label: str, ref, gen, path: str = "", errors: list | None = None) -> list:
    """Recursively compare two YAML-parsed objects and collect differences."""
    if errors is None:
        errors = []

    if type(ref) != type(gen):
        errors.append(
            f"{path}: TYPE MISMATCH — {type(ref).__name__} vs {type(gen).__name__}"
        )
        return errors

    if isinstance(ref, dict):
        ref_keys = set(ref.keys())
        gen_keys = set(gen.keys())
        only_ref = ref_keys - gen_keys
        only_gen = gen_keys - ref_keys
        if only_ref:
            errors.append(f"{path}: MISSING IN GENERATED — {sorted(only_ref)}")
        if only_gen:
            errors.append(f"{path}: EXTRA IN GENERATED — {sorted(only_gen)}")
        common = ref_keys & gen_keys
        for key in sorted(common):
            deep_diff(label, ref[key], gen[key], f"{path}.{key}", errors)
    elif isinstance(ref, list):
        if len(ref) != len(gen):
            errors.append(f"{path}: LIST LENGTH MISMATCH — {len(ref)} vs {len(gen)}")
        else:
            for i, (r, g) in enumerate(zip(ref, gen)):
                deep_diff(label, r, g, f"{path}[{i}]", errors)
    elif isinstance(ref, str):
        if ref != gen:
            errors.append(f"{path}: STRING MISMATCH — {ref!r} vs {gen!r}")
    elif isinstance(ref, (int, float)):
        if ref != gen:
            errors.append(f"{path}: NUMBER MISMATCH — {ref!r} vs {gen!r}")
    elif isinstance(ref, bool):
        if ref != gen:
            errors.append(f"{path}: BOOL MISMATCH — {ref!r} vs {gen!r}")
    elif ref is None:
        if gen is not None:
            errors.append(f"{path}: NULL MISMATCH — None vs {gen!r}")
    else:
        if ref != gen:
            errors.append(f"{path}: VALUE MISMATCH — {ref!r} vs {gen!r}")

    return errors


def _is_desc_only(err: str) -> bool:
    """True if the error is a description-only string mismatch."""
    return re.match(r".*\.description: STRING MISMATCH", err) is not None


def _is_aprop(err: str) -> bool:
    """True if the error is about additionalProperties."""
    return "additionalPropert" in err


def _categorize_errors(errors: list[str]) -> dict[str, list[str]]:
    """Split errors into description-only, additionalProperties, and structural."""
    desc: list[str] = []
    aprop: list[str] = []
    struct: list[str] = []
    for e in errors:
        if _is_desc_only(e):
            desc.append(e)
        elif _is_aprop(e):
            aprop.append(e)
        else:
            struct.append(e)
    return {"desc": desc, "aprop": aprop, "struct": struct}


def compare_section(label: str, ref: dict, gen: dict, path: str, errors: list) -> None:
    """Compare a top-level section."""
    section_errors = deep_diff(label, ref.get(path, {}), gen.get(path, {}), path)
    if section_errors:
        print(f"\n  {label} ({red(str(len(section_errors)))} diff(s)):")
        for e in section_errors:
            print(f"    - {dim(e)}")
    else:
        print(f"  {label}: {green('✓ IDENTICAL')}")


MARKER_LINE = (
    "  # Schemas removed because they are neither direct nor transitive requirements:"
)

TEMPLATE_FILE = "tools/templates/openapi/workload-management-api-1.0.0.openapi.yaml"

# Pattern for standardized INLINED comments: <name> INLINED into <target>(OpenAPI)[/<class>(LinkML)]
INLINED_PATTERN = re.compile(
    r"#\s*-\s*(\S+)\s+INLINED\s+into\s+\S+\(OpenAPI\)(?:/\S+\(LinkML\))?"
)


def get_inlined_schemas() -> set[str]:
    """Scan the template file for INLINED comment markers and return schema names."""
    path = ROOT / TEMPLATE_FILE
    if not path.exists():
        return set()
    result: set[str] = set()
    with open(path) as f:
        for line in f:
            m = INLINED_PATTERN.search(line)
            if m:
                result.add(m.group(1))
    return result


def get_xlinkml_renames() -> dict[str, str]:
    """Extract x-linkml-source renames from the template file."""
    renames: dict[str, str] = {}
    path = ROOT / TEMPLATE_FILE
    if not path.exists():
        return renames
    with open(path) as f:
        tpl = yaml.safe_load(f)
    schemas = tpl.get("components", {}).get("schemas", {})
    for name, spec in schemas.items():
        src = spec.get("x-linkml-source")
        if src and src != name:
            renames[name] = src
    return renames


def find_rename_candidates(
    ref_schemas: dict, gen_schemas: dict
) -> list[tuple[str, str, float]]:
    """Heuristically match missing ref schemas to extra gen schemas by structure.

    Compares property sets, required fields, and type (excluding descriptions).
    Returns (ref_name, gen_name, score) tuples sorted by descending score.
    """

    def _signature(name: str, s: dict) -> dict:
        props = (
            set(s.get("properties", {}).keys())
            if isinstance(s.get("properties"), dict)
            else set()
        )
        req = set(s.get("required", []))
        typ = s.get("type")
        return {"props": props, "req": req, "type": typ, "name": name}

    ref_sigs = {n: _signature(n, s) for n, s in ref_schemas.items()}
    gen_sigs = {n: _signature(n, s) for n, s in gen_schemas.items()}

    candidates: list[tuple[str, str, float]] = []
    for rn, rs in ref_sigs.items():
        if rn in gen_schemas:
            continue
        for gn, gs in gen_sigs.items():
            if gn in ref_schemas:
                continue
            if rs["type"] != gs["type"]:
                continue
            prop_union = rs["props"] | gs["props"]
            if not prop_union:
                continue
            prop_score = len(rs["props"] & gs["props"]) / len(prop_union)
            req_score = (
                1.0
                if not rs["req"] and not gs["req"]
                else len(rs["req"] & gs["req"]) / len(rs["req"] | gs["req"])
            )
            score = 0.7 * prop_score + 0.3 * req_score
            if score >= 0.3:
                candidates.append((rn, gn, round(score, 3)))
    candidates.sort(key=lambda x: -x[2])
    return candidates


def get_not_needed_schemas() -> set[str]:
    """Scan the generated file text for a block comment listing removed schemas.

    Looks for a line matching MARKER_LINE, then collects every following
    ``  # <name>`` line until a non-matching line is encountered.
    """
    path = ROOT / GENERATED_FILE
    if not path.exists():
        return set()
    result = set()
    in_block = False
    schema_pat = re.compile(r"^  # (\S+)")
    with open(path) as f:
        for line in f:
            if line.rstrip("\n") == MARKER_LINE:
                in_block = True
                continue
            if in_block:
                m = schema_pat.match(line)
                if m:
                    result.add(m.group(1))
                else:
                    break
    return result


def _schema_signature(s: dict) -> dict:
    """Extract a comparable signature from a schema dict, ignoring descriptions."""
    if not isinstance(s, dict):
        return {}
    props = s.get("properties", {})
    return {
        "type": s.get("type"),
        "properties": set(props.keys()) if isinstance(props, dict) else set(),
        "required": set(s.get("required", [])),
        "enum": sorted(s.get("enum", [])) if isinstance(s.get("enum"), list) else [],
        "additionalProperties": isinstance(s.get("additionalProperties"), dict)
        or s.get("additionalProperties") is True,
    }


def _collect_inline_properties(ref_schemas: dict) -> list[tuple[str, str, dict]]:
    """Walk all pre-draft schemas and collect inline object properties.

    Only collects nested properties (not the top-level schema itself)
    to avoid false matches where a gen schema is structurally similar
    to a parent schema that happens to share property names.

    Returns [(parent_name, property_path, inline_schema), ...] where
    property_path is e.g. 'properties.foo.items' for nested inline objects.
    """
    results: list[tuple[str, str, dict]] = []

    def _walk(obj, parent: str, path: str, depth: int = 0):
        if depth > 8:
            return
        if isinstance(obj, dict):
            # Recurse into properties (skip top-level by requiring depth > 0 for the object itself)
            props = obj.get("properties", {})
            if isinstance(props, dict):
                for pname, pval in props.items():
                    if isinstance(pval, dict) and "$ref" not in pval:
                        # Collect this inline property
                        if "properties" in pval or "enum" in pval or "items" in pval:
                            results.append((parent, f"{path}.properties.{pname}", pval))
                        _walk(pval, parent, f"{path}.properties.{pname}", depth + 1)
            # Recurse into items
            items = obj.get("items", {})
            if isinstance(items, dict) and "$ref" not in items:
                if "properties" in items or "enum" in items:
                    results.append((parent, f"{path}.items", items))
                _walk(items, parent, f"{path}.items", depth + 1)
            # Recurse into additionalProperties
            ap = obj.get("additionalProperties", {})
            if isinstance(ap, dict) and "$ref" not in ap:
                if "properties" in ap or "enum" in ap:
                    results.append((parent, f"{path}.additionalProperties", ap))
                _walk(ap, parent, f"{path}.additionalProperties", depth + 1)
            # Recurse into anyOf / oneOf / allOf
            for comb in ("anyOf", "oneOf", "allOf"):
                for i, entry in enumerate(obj.get(comb, [])):
                    if isinstance(entry, dict) and "$ref" not in entry:
                        if "properties" in entry or "enum" in entry:
                            results.append((parent, f"{path}.{comb}[{i}]", entry))
                        _walk(entry, parent, f"{path}.{comb}[{i}]", depth + 1)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, dict) and "$ref" not in item:
                    if "properties" in item or "enum" in item:
                        results.append((parent, f"{path}[{i}]", item))
                    _walk(item, parent, f"{path}[{i}]", depth + 1)

    for schema_name, schema_def in ref_schemas.items():
        if isinstance(schema_def, dict):
            _walk(schema_def, schema_name, schema_name)

    return results


def find_inlined_candidates(
    ref_schemas: dict, gen_schemas: dict, extra_gen: set[str]
) -> list[tuple[str, str, float]]:
    """For each extra gen schema, find a matching inline property in the pre-draft.

    Returns [(gen_name, parent.property_path, score), ...] sorted by descending score.
    """
    inline_props = _collect_inline_properties(ref_schemas)
    gen_sigs = {
        n: _schema_signature(s) for n, s in gen_schemas.items() if n in extra_gen
    }
    if not gen_sigs:
        return []

    candidates: list[tuple[str, str, float]] = []
    for gen_name, gs in gen_sigs.items():
        for parent_name, prop_path, inline_def in inline_props:
            rs = _schema_signature(inline_def)
            if rs["type"] and rs["type"] != gs["type"]:
                continue
            if rs["enum"] and rs["enum"] != gs["enum"]:
                continue
            prop_union = rs["properties"] | gs["properties"]
            if not prop_union:
                continue
            prop_score = len(rs["properties"] & gs["properties"]) / len(prop_union)
            req_score = (
                1.0
                if not rs["required"] and not gs["required"]
                else len(rs["required"] & gs["required"])
                / len(rs["required"] | gs["required"])
            )
            score = round(0.7 * prop_score + 0.3 * req_score, 3)
            candidates.append((gen_name, prop_path, score))

    candidates.sort(key=lambda x: -x[2])
    return candidates


def _resolve_schema_name(
    raw: str, gen_schemas: dict, xlinkml_renames: dict
) -> str | None:
    """Resolve an OpenAPI or LinkML name to the generated schema name."""
    if raw in gen_schemas:
        return raw
    # Check if it's a LinkML name → find the OpenAPI name via renames
    for openapi_name, linkml_name in xlinkml_renames.items():
        if linkml_name == raw or linkml_name.split(".")[0] == raw:
            return openapi_name
    # Check dotted path: Class.slot → synthetic key
    for openapi_name, linkml_name in xlinkml_renames.items():
        if linkml_name == raw:
            return openapi_name
    return None


def _collect_refs(obj, results: set[str], prefix: str = "#/components/schemas/"):
    """Recursively collect all $ref target names from a schema definition."""
    if isinstance(obj, dict):
        if (
            "$ref" in obj
            and isinstance(obj["$ref"], str)
            and obj["$ref"].startswith(prefix)
        ):
            results.add(obj["$ref"].replace(prefix, ""))
        for v in obj.values():
            _collect_refs(v, results, prefix)
    elif isinstance(obj, list):
        for item in obj:
            _collect_refs(item, results, prefix)


def _find_referers(
    schema_name: str, gen_schemas: dict, gen_paths: dict
) -> tuple[list[str], list[str]]:
    """Find all paths and schemas that reference the given schema."""
    path_refs: list[str] = []
    schema_refs: list[str] = []
    target = f"#/components/schemas/{schema_name}"

    # Check paths
    for path, methods in gen_paths.items():
        for method, spec in methods.items():

            def _check(obj):
                if isinstance(obj, dict):
                    if "$ref" in obj and obj["$ref"] == target:
                        path_refs.append(f"{method.upper()} {path}")
                        return
                    for v in obj.values():
                        _check(v)
                elif isinstance(obj, list):
                    for item in obj:
                        _check(item)

            _check(spec)

    # Check schemas
    for name, schema in gen_schemas.items():
        if name == schema_name:
            continue
        found: set[str] = set()
        _collect_refs(schema, found)
        if schema_name in found:
            schema_refs.append(name)

    # Deduplicate and sort
    return sorted(set(path_refs)), sorted(set(schema_refs))


def _show_schema_detail(raw_name: str, show_yaml: bool = False) -> None:
    """Show detailed information about a single schema."""
    ref = get_pre_draft_spec()
    gen = get_generated_spec()
    xlinkml_renames = get_xlinkml_renames()
    gen_schemas = gen.get("components", {}).get("schemas", {})
    ref_schemas = ref.get("components", {}).get("schemas", {})
    gen_paths = gen.get("paths", {})
    ref_comp = ref.get("components", {})
    gen_comp = gen.get("components", {})

    ref_keys = set(ref_schemas.keys())
    gen_keys = set(gen_schemas.keys())
    only_ref = ref_keys - gen_keys
    only_gen = gen_keys - ref_keys
    common = ref_keys & gen_keys

    schema_name = _resolve_schema_name(raw_name, gen_schemas, xlinkml_renames)
    if schema_name is None:
        print(f"{red('Schema not found:')} {raw_name}")
        print(f"  {dim('Try an OpenAPI schema name or a LinkML class/type name.')}")
        print(f"  {dim('OpenAPI names:')} {', '.join(sorted(gen_schemas.keys()))}")
        return

    linkml_src = None
    for on, ln in xlinkml_renames.items():
        if on == schema_name:
            linkml_src = ln
            break

    print(f"\n{bold(schema_name)}")
    if linkml_src:
        print(f"  LinkML source: {dim(linkml_src)}")

    if schema_name in gen_schemas:
        gen_s = gen_schemas[schema_name]
        refs_from: set[str] = set()
        _collect_refs(gen_s, refs_from)
        path_refs, schema_refs = _find_referers(schema_name, gen_schemas, gen_paths)

        # Status
        if schema_name in common:
            s_errors = deep_diff("", ref_schemas[schema_name], gen_s, schema_name)
            cats = _categorize_errors(s_errors)
            status = (
                f"{red(str(len(s_errors)))} diff(s)" if s_errors else green("identical")
            )
            print(f"  Status: {status}")
            if cats["desc"]:
                print(f"    {dim('Description-only')} ({len(cats['desc'])}):")
                for e in cats["desc"]:
                    print(f"      - {dim(e)}")
            if cats["aprop"]:
                print(f"    {yellow('additionalProperties')} ({len(cats['aprop'])}):")
                for e in cats["aprop"]:
                    print(f"      - {yellow(e)}")
            if cats["struct"]:
                print(f"    {red('Structural')} ({len(cats['struct'])}):")
                for e in cats["struct"]:
                    print(f"      - {red(e)}")
        elif schema_name in only_gen:
            print(f"  Status: {yellow('EXTRA — not in pre-draft')}")
        elif schema_name in only_ref:
            print(f"  Status: {red('MISSING — not in generated output')}")
        else:
            print(f"  Status: {green('not in comparison')}")

        # Referers (paths)
        if path_refs:
            print(f"  {dim('Referenced by endpoints')} ({len(path_refs)}):")
            for pr in path_refs:
                print(f"    {green(pr)}")
        else:
            print(f"  {dim('Referenced by endpoints:')} {dim('none')}")

        # Referers (schemas)
        if schema_refs:
            print(f"  {dim('Referenced by schemas')} ({len(schema_refs)}):")
            for sr in schema_refs:
                print(f"    {sr}")
        else:
            print(f"  {dim('Referenced by schemas:')} {dim('none')}")

        # References from this schema
        if refs_from:
            print(f"  {dim('References to other schemas')} ({len(refs_from)}):")
            for rf in sorted(refs_from):
                print(f"    {rf}")
        else:
            print(f"  {dim('References to other schemas:')} {dim('none')}")

        # Inline / extra context
        if schema_name in only_gen:
            candidates = find_inlined_candidates(
                ref_schemas, {schema_name: gen_s}, {schema_name}
            )
            if candidates:
                best = max(candidates, key=lambda x: x[2])
                print(
                    f"  {yellow('Inferred inlined')} in pre-draft at {best[1]} (score {best[2]})"
                )
        elif schema_name in common:
            pre_s = ref_schemas.get(schema_name, {})
            props = pre_s.get("properties", {})
            if isinstance(props, dict):
                inlined_props = [
                    k
                    for k, v in props.items()
                    if isinstance(v, dict) and "$ref" not in v and "properties" in v
                ]
                if inlined_props:
                    print(
                        f"  {dim('Pre-draft inlined properties:')} {', '.join(inlined_props)}"
                    )

        # Property-level comparison
        if schema_name in common:
            pre_s = ref_schemas[schema_name]
            gen_props = gen_s.get("properties", {})
            pre_props = pre_s.get("properties", {})
            if isinstance(gen_props, dict) and isinstance(pre_props, dict):
                gen_keys_set = set(gen_props.keys())
                pre_keys_set = set(pre_props.keys())
                only_pre = pre_keys_set - gen_keys_set
                only_gen_p = gen_keys_set - pre_keys_set
                if only_pre:
                    print(
                        f"  {red('Properties only in pre-draft:')} {sorted(only_pre)}"
                    )
                if only_gen_p:
                    print(
                        f"  {yellow('Properties only in generated:')} {sorted(only_gen_p)}"
                    )

        # YAML dump
        if show_yaml:
            print(f"\n{dim('─' * 40)}")
            pre_s = (
                ref_schemas.get(schema_name, ref_schemas.get(raw_name))
                if schema_name in common
                else None
            )
            gen_s = gen_schemas.get(schema_name)
            if pre_s:
                print(f"\n{bold('Pre-draft')} ({schema_name}):")
                print(
                    yaml.dump(
                        pre_s,
                        default_flow_style=False,
                        sort_keys=False,
                        allow_unicode=True,
                    ).rstrip()
                )
            if gen_s:
                print(f"\n{bold('Generated')} ({schema_name}):")
                print(
                    yaml.dump(
                        gen_s,
                        default_flow_style=False,
                        sort_keys=False,
                        allow_unicode=True,
                    ).rstrip()
                )

    else:
        if schema_name in only_ref:
            print(f"\n  {bold(schema_name)}")
            print(f"  Status: {red('MISSING — in pre-draft but not generated')}")
            pre_s = ref_schemas.get(schema_name, {})
            if pre_s:
                print(f"  {dim('Pre-draft definition:')}")
                print(f"    type: {pre_s.get('type', 'N/A')}")
                props = pre_s.get("properties", {})
                if isinstance(props, dict):
                    for pk, pv in props.items():
                        ref_type = (
                            pv.get("type", "object") if isinstance(pv, dict) else "N/A"
                        )
                        print(f"    {pk}: {ref_type}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare pre-draft vs generated OpenAPI spec"
    )
    parser.add_argument(
        "--schema",
        "-s",
        help="Show verbose details for a single schema only (name in generated output)",
    )
    parser.add_argument(
        "--yaml",
        "-y",
        action="store_true",
        help="Show YAML of both pre-draft and generated schemas (use with -s)",
    )
    args = parser.parse_args()

    # Single-schema mode: skip everything and show only the schema detail
    if args.schema:
        _show_schema_detail(args.schema, args.yaml)
        return

    print(cyan("=" * 60))
    print(cyan("OpenAPI Spec Validation: pre-draft vs generated"))
    print(cyan("=" * 60))

    ref = get_pre_draft_spec()
    gen = get_generated_spec()

    # 1. Info
    print(f"\n{cyan('--- Top-level ---')}")
    for key in ["openapi", "info"]:
        compare_section(key, ref, gen, key, [])

    # 2. Servers
    compare_section("servers", ref, gen, "servers", [])

    # 3. Security
    compare_section("security", ref, gen, "security", [])

    # 4. Paths
    print(f"\n{cyan('--- Paths ---')}")
    ref_paths = ref.get("paths", {})
    gen_paths = gen.get("paths", {})
    ref_pkeys = set(ref_paths.keys())
    gen_pkeys = set(gen_paths.keys())
    only_ref_p = ref_pkeys - gen_pkeys
    only_gen_p = gen_pkeys - ref_pkeys
    common_p = ref_pkeys & gen_pkeys

    if only_ref_p:
        print(
            f"  {red('MISSING IN GENERATED')} ({len(only_ref_p)}): {sorted(only_ref_p)}"
        )
    if only_gen_p:
        print(
            f"  {yellow('EXTRA IN GENERATED')} ({len(only_gen_p)}): {sorted(only_gen_p)}"
        )

    for path in sorted(common_p):
        ref_methods = ref_paths[path]
        gen_methods = gen_paths[path]
        ref_mkeys = set(ref_methods.keys())
        gen_mkeys = set(gen_methods.keys())
        only_ref_m = ref_mkeys - gen_mkeys
        only_gen_m = gen_mkeys - ref_mkeys

        if only_ref_m or only_gen_m:
            print(
                f"  {yellow(path)}: METHOD DIFF — ref={sorted(ref_mkeys)} gen={sorted(gen_mkeys)}"
            )
        else:
            all_method_ok = True
            for method in sorted(ref_mkeys):
                errs = deep_diff(
                    path, ref_methods[method], gen_methods[method], f"{path}.{method}"
                )
                if errs:
                    all_method_ok = False
                    print(f"  {path}.{method}: {red(str(len(errs)))} diff(s)")
                    for e in errs:
                        print(f"    - {dim(e)}")
            if all_method_ok:
                print(f"  {path}: {green('✓ IDENTICAL')}")

    # 5. Components (excluding schemas — handled separately)
    print(f"\n{cyan('--- Components (non-schemas) ---')}")
    ref_comp = ref.get("components", {})
    gen_comp = gen.get("components", {})
    comp_keys = set(ref_comp.keys()) | set(gen_comp.keys())
    for ck in sorted(comp_keys):
        if ck == "schemas":
            continue
        compare_section(f"components.{ck}", ref_comp, gen_comp, ck, [])

    # 6. Schemas (detailed)
    print(f"\n{cyan('--- components/schemas ---')}")
    ref_schemas = ref_comp.get("schemas", {})
    gen_schemas = gen_comp.get("schemas", {})
    not_needed = get_not_needed_schemas()
    inlined = get_inlined_schemas()
    xlinkml_renames = get_xlinkml_renames()
    rename_candidates = find_rename_candidates(ref_schemas, gen_schemas)

    ref_keys = set(ref_schemas.keys())
    gen_keys = set(gen_schemas.keys())
    only_ref = ref_keys - gen_keys
    only_gen = gen_keys - ref_keys
    common = ref_keys & gen_keys
    intentionally_omitted = (only_ref & not_needed) | (only_ref & inlined)
    truly_missing = only_ref - not_needed - inlined

    inlined_candidates = find_inlined_candidates(ref_schemas, gen_schemas, only_gen)
    # Deduplicate: pick the best match per gen schema
    best_per_schema: dict[str, tuple[str, float]] = {}
    for gen_name, prop_path, score in inlined_candidates:
        prev = best_per_schema.get(gen_name)
        if prev is None or score > prev[1]:
            best_per_schema[gen_name] = (prop_path, score)
    high_scoring_inlined = []
    explained_extra: set[str] = set()
    for gen_name, (prop_path, score) in sorted(
        best_per_schema.items(), key=lambda x: -x[1][1]
    ):
        if score >= 0.9:
            high_scoring_inlined.append((gen_name, prop_path, score))
            explained_extra.add(gen_name)
    unexplained_extra = only_gen - explained_extra

    print(
        f"\n  Schemas ({bold(str(len(ref_keys)))} ref, {bold(str(len(gen_keys)))} gen, {bold(str(len(not_needed)))} NOT-NEEDED, {bold(str(len(inlined)))} INLINED):"
    )

    if xlinkml_renames:
        print(f"    {dim('x-linkml-source RENAMES')} ({len(xlinkml_renames)}):")
        for openapi_name, linkml_name in sorted(xlinkml_renames.items()):
            print(f"      {openapi_name} ← {linkml_name}")

    if intentionally_omitted:
        not_needed_only = intentionally_omitted & not_needed
        inlined_only = intentionally_omitted & inlined
        if not_needed_only:
            print(
                f"    {dim('NOT-NEEDED')} ({len(not_needed_only)}): {sorted(not_needed_only)}"
            )
        if inlined_only:
            print(
                f"    {dim('INLINED SUBSCHEMAS')} ({len(inlined_only)}): {sorted(inlined_only)}"
            )

    if truly_missing:
        print(
            f"    {red('MISSING IN GENERATED')} ({len(truly_missing)}): {sorted(truly_missing)}"
        )

    if high_scoring_inlined:
        print(f"    {yellow('INFERRED INLINED')} ({len(high_scoring_inlined)}):")
        for gen_name, prop_path, score in sorted(
            high_scoring_inlined, key=lambda x: -x[2]
        ):
            print(f"      {gen_name} inlined into {prop_path} (score {score})")

    if unexplained_extra:
        print(
            f"    {yellow('EXTRA IN GENERATED')} ({len(unexplained_extra)}): {sorted(unexplained_extra)}"
        )

    if rename_candidates:
        print(
            f"    {dim('RENAME CANDIDATES')} (missing → extra, by structural similarity):"
        )
        shown = 0
        for ref_name, gen_name, score in rename_candidates:
            if ref_name in truly_missing and gen_name in unexplained_extra:
                print(f"      {ref_name} ↔ {gen_name} (score {score})")
                shown += 1
                if shown >= 5:
                    print(f"      ... ({len(rename_candidates) - 5} more)")
                    break

    elif common:
        # ── Full summary with categorization ────────────────────
        all_aprop_schemas: set[str] = set()
        changed_names: list[str] = []
        for name in sorted(common):
            ref_s = ref_schemas[name]
            gen_s = gen_schemas[name]
            s_errors = deep_diff("", ref_s, gen_s, name)
            if not s_errors:
                continue
            changed_names.append(name)
            cats = _categorize_errors(s_errors)
            if cats["aprop"]:
                all_aprop_schemas.add(name)
            # Only show this schema in detail if it has structural changes
            if cats["struct"] or (
                cats["desc"] and not cats["aprop"] and not cats["struct"]
            ):
                non_desc = len(s_errors) - len(cats["desc"])
                if non_desc:
                    print(f"    {name}: {red(str(non_desc))} non-description diff(s)")
                else:
                    print(
                        f"    {name}: {dim('description-only')} ({len(cats['desc'])} diff(s))"
                    )

        # Grouped additionalProperties report
        if all_aprop_schemas:
            print(
                f"    {yellow('additionalProperties:')} present in {len(all_aprop_schemas)} schema(s)"
            )
            print(
                f"      {dim('added by LinkML JSON Schema generator (additionalProperties: false)')}"
            )
            print(f"      {dim('affected:')} {', '.join(sorted(all_aprop_schemas))}")

        unchanged = len(common) - len(changed_names)
        print(
            f"    {dim('Common schemas:')} {green(str(unchanged))} identical, {yellow(str(len(changed_names)))} changed"
        )
    else:
        print(f"    {green('No common schemas')}")

    print(f"\n{cyan('=' * 60)}")
    total_errors = len(deep_diff("", ref, gen, ""))
    if total_errors == 0:
        print(f"{green('RESULT: FULLY IDENTICAL ✓')}")
    else:
        print(f"{red(f'RESULT: {total_errors} difference(s) found')}")
    print(cyan("=" * 60))


if __name__ == "__main__":
    main()
