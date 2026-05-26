from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from src.converter import (
    TEMPLATE_PREFIX,
    _find_refs,
    _rewrite_ref_value,
    collect_dependencies,
    extract_definition,
    generate_json_schema,
    normalize_nullable,
    rewrite_refs,
    strip_template_prefix,
)


# ─────────────────────────────────────────────────────────────────────────────
# _rewrite_ref_value
# ─────────────────────────────────────────────────────────────────────────────

class TestRewriteRefValue:
    def test_rewrites_defs_ref(self):
        assert _rewrite_ref_value("#/$defs/MyClass") == "#/components/schemas/MyClass"

    def test_leaves_components_ref_unchanged(self):
        ref = "#/components/schemas/MyClass"
        assert _rewrite_ref_value(ref) == ref

    def test_leaves_external_ref_unchanged(self):
        ref = "https://example.com/schema.json"
        assert _rewrite_ref_value(ref) == ref

    def test_leaves_relative_ref_unchanged(self):
        ref = "./other.yaml#/$defs/Foo"
        assert _rewrite_ref_value(ref) == ref

    def test_idempotent_on_already_rewritten(self):
        ref = "#/components/schemas/Foo"
        assert _rewrite_ref_value(ref) == ref


# ─────────────────────────────────────────────────────────────────────────────
# rewrite_refs
# ─────────────────────────────────────────────────────────────────────────────

class TestRewriteRefs:
    def test_rewrites_simple_ref(self):
        schema = {"$ref": "#/$defs/Foo"}
        assert rewrite_refs(schema) == {"$ref": "#/components/schemas/Foo"}

    def test_ref_with_sibling_wrapped_in_allof(self):
        schema = {"$ref": "#/$defs/Foo", "description": "A foo"}
        result = rewrite_refs(schema)
        assert result == {
            "allOf": [{"$ref": "#/components/schemas/Foo"}],
            "description": "A foo",
        }

    def test_ref_with_multiple_siblings_wrapped_in_allof(self):
        schema = {"$ref": "#/$defs/Foo", "description": "desc", "title": "Foo"}
        result = rewrite_refs(schema)
        assert "allOf" in result
        assert result["allOf"] == [{"$ref": "#/components/schemas/Foo"}]
        assert result["description"] == "desc"
        assert result["title"] == "Foo"

    def test_ref_without_siblings_not_wrapped(self):
        schema = {"$ref": "#/$defs/Foo"}
        result = rewrite_refs(schema)
        assert "allOf" not in result
        assert result == {"$ref": "#/components/schemas/Foo"}

    def test_strips_const(self):
        schema = {"type": "string", "const": "fixed"}
        result = rewrite_refs(schema)
        assert "const" not in result
        assert result["type"] == "string"

    def test_const_only_schema_becomes_empty(self):
        schema = {"const": "value"}
        result = rewrite_refs(schema)
        assert result == {}

    def test_nested_ref_rewritten(self):
        schema = {
            "type": "object",
            "properties": {
                "foo": {"$ref": "#/$defs/Foo"},
            },
        }
        result = rewrite_refs(schema)
        assert result["properties"]["foo"] == {"$ref": "#/components/schemas/Foo"}

    def test_ref_in_list_rewritten(self):
        schema = [{"$ref": "#/$defs/A"}, {"$ref": "#/$defs/B"}]
        result = rewrite_refs(schema)
        assert result == [
            {"$ref": "#/components/schemas/A"},
            {"$ref": "#/components/schemas/B"},
        ]

    def test_passthrough_string(self):
        assert rewrite_refs("hello") == "hello"

    def test_passthrough_integer(self):
        assert rewrite_refs(42) == 42

    def test_idempotent_on_components_ref(self):
        schema = {"$ref": "#/components/schemas/Foo"}
        assert rewrite_refs(schema) == schema

    def test_deeply_nested_ref(self):
        schema = {
            "properties": {
                "a": {
                    "properties": {
                        "b": {"$ref": "#/$defs/Deep"}
                    }
                }
            }
        }
        result = rewrite_refs(schema)
        assert (
            result["properties"]["a"]["properties"]["b"]["$ref"]
            == "#/components/schemas/Deep"
        )

    def test_allof_items_rewritten(self):
        schema = {"allOf": [{"$ref": "#/$defs/Base"}]}
        result = rewrite_refs(schema)
        assert result == {"allOf": [{"$ref": "#/components/schemas/Base"}]}


# ─────────────────────────────────────────────────────────────────────────────
# normalize_nullable
# ─────────────────────────────────────────────────────────────────────────────

class TestNormalizeNullable:

    # ── Rule 1: type arrays ──────────────────────────────────────────────────

    def test_type_array_with_null(self):
        schema = {"type": ["string", "null"]}
        result = normalize_nullable(schema)
        assert result == {"type": "string", "nullable": True}

    def test_type_array_null_only(self):
        schema = {"type": ["null"]}
        result = normalize_nullable(schema)
        assert "type" not in result
        assert result["nullable"] is True

    def test_type_array_without_null_unchanged(self):
        schema = {"type": ["string", "integer"]}
        result = normalize_nullable(schema)
        # No null → no nullable added, but multiple types become anyOf
        assert "nullable" not in result
        assert "anyOf" in result
        assert {"type": "string"} in result["anyOf"]
        assert {"type": "integer"} in result["anyOf"]

    def test_type_array_multiple_non_null_with_null(self):
        schema = {"type": ["string", "integer", "null"]}
        result = normalize_nullable(schema)
        assert result["nullable"] is True
        assert "type" not in result
        assert "anyOf" in result
        assert {"type": "string"} in result["anyOf"]
        assert {"type": "integer"} in result["anyOf"]

    def test_type_string_unchanged(self):
        schema = {"type": "string"}
        result = normalize_nullable(schema)
        assert result == {"type": "string"}

    # ── Rule 2: anyOf with null ──────────────────────────────────────────────

    def test_anyof_ref_and_null_becomes_allof_nullable(self):
        schema = {
            "anyOf": [
                {"$ref": "#/components/schemas/Foo"},
                {"type": "null"},
            ]
        }
        result = normalize_nullable(schema)
        assert result["nullable"] is True
        assert result["allOf"] == [{"$ref": "#/components/schemas/Foo"}]
        assert "anyOf" not in result

    def test_anyof_inline_schema_and_null_inlined(self):
        schema = {
            "anyOf": [
                {"type": "string", "minLength": 1},
                {"type": "null"},
            ]
        }
        result = normalize_nullable(schema)
        assert result["nullable"] is True
        assert result["type"] == "string"
        assert result["minLength"] == 1
        assert "anyOf" not in result

    def test_anyof_multiple_non_null_with_null(self):
        schema = {
            "anyOf": [
                {"type": "string"},
                {"type": "integer"},
                {"type": "null"},
            ]
        }
        result = normalize_nullable(schema)
        assert result["nullable"] is True
        assert len(result["anyOf"]) == 2
        assert {"type": "null"} not in result["anyOf"]

    def test_anyof_null_only_removes_anyof(self):
        schema = {"anyOf": [{"type": "null"}]}
        result = normalize_nullable(schema)
        assert "anyOf" not in result
        assert result["nullable"] is True

    def test_anyof_without_null_unchanged(self):
        schema = {
            "anyOf": [{"type": "string"}, {"type": "integer"}]
        }
        result = normalize_nullable(schema)
        assert "nullable" not in result
        assert result["anyOf"] == [{"type": "string"}, {"type": "integer"}]

    # ── Recursion ────────────────────────────────────────────────────────────

    def test_nested_nullable_normalised(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": ["string", "null"]},
            },
        }
        result = normalize_nullable(schema)
        assert result["properties"]["name"] == {"type": "string", "nullable": True}

    def test_list_items_normalised(self):
        schema = [{"type": ["string", "null"]}, {"type": "integer"}]
        result = normalize_nullable(schema)
        assert result[0] == {"type": "string", "nullable": True}
        assert result[1] == {"type": "integer"}

    def test_passthrough_string(self):
        assert normalize_nullable("hello") == "hello"

    def test_passthrough_integer(self):
        assert normalize_nullable(42) == 42

    def test_existing_description_preserved_when_inlining(self):
        """description on the outer schema must not be overwritten by inlined fields."""
        schema = {
            "description": "outer",
            "anyOf": [
                {"type": "string", "description": "inner"},
                {"type": "null"},
            ],
        }
        result = normalize_nullable(schema)
        assert result["description"] == "outer"
        assert result["nullable"] is True


# ─────────────────────────────────────────────────────────────────────────────
# strip_template_prefix
# ─────────────────────────────────────────────────────────────────────────────

class TestStripTemplatePrefix:
    def test_strips_prefix(self):
        schema = {"description": "[TEMPLATE] Some description"}
        result = strip_template_prefix(schema)
        assert result["description"] == "Some description"

    def test_strips_prefix_and_whitespace(self):
        schema = {"description": "[TEMPLATE]   Padded description"}
        result = strip_template_prefix(schema)
        assert result["description"] == "Padded description"

    def test_no_prefix_unchanged(self):
        schema = {"description": "Normal description"}
        result = strip_template_prefix(schema)
        assert result["description"] == "Normal description"

    def test_no_description_unchanged(self):
        schema = {"type": "string"}
        result = strip_template_prefix(schema)
        assert result == {"type": "string"}

    def test_non_string_description_unchanged(self):
        schema = {"description": 42}
        result = strip_template_prefix(schema)
        assert result["description"] == 42

    def test_returns_new_dict_not_mutated(self):
        schema = {"description": "[TEMPLATE] desc"}
        result = strip_template_prefix(schema)
        assert result is not schema


# ─────────────────────────────────────────────────────────────────────────────
# _find_refs
# ─────────────────────────────────────────────────────────────────────────────

class TestFindRefs:
    def test_finds_simple_ref(self):
        obj = {"$ref": "#/$defs/Foo"}
        assert _find_refs(obj) == ["#/$defs/Foo"]

    def test_finds_nested_ref(self):
        obj = {"properties": {"a": {"$ref": "#/$defs/Bar"}}}
        assert _find_refs(obj) == ["#/$defs/Bar"]

    def test_finds_multiple_refs(self):
        obj = {
            "properties": {
                "a": {"$ref": "#/$defs/A"},
                "b": {"$ref": "#/$defs/B"},
            }
        }
        refs = _find_refs(obj)
        assert set(refs) == {"#/$defs/A", "#/$defs/B"}

    def test_finds_refs_in_list(self):
        obj = [{"$ref": "#/$defs/X"}, {"$ref": "#/$defs/Y"}]
        assert set(_find_refs(obj)) == {"#/$defs/X", "#/$defs/Y"}

    def test_no_refs_returns_empty(self):
        obj = {"type": "string"}
        assert _find_refs(obj) == []

    def test_string_returns_empty(self):
        assert _find_refs("hello") == []

    def test_finds_ref_in_anyof(self):
        obj = {"anyOf": [{"$ref": "#/$defs/Foo"}, {"type": "null"}]}
        assert "#/$defs/Foo" in _find_refs(obj)


# ─────────────────────────────────────────────────────────────────────────────
# extract_definition
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractDefinition:
    def _make_schema(self, defs: dict) -> dict:
        return {"$defs": defs}

    def test_extracts_simple_class(self):
        json_schema = self._make_schema({
            "MyClass": {"type": "object", "properties": {"id": {"type": "string"}}}
        })
        result = extract_definition(json_schema, "MyClass")
        assert result["type"] == "object"

    def test_raises_key_error_for_missing_name(self):
        json_schema = self._make_schema({"Other": {"type": "object"}})
        with pytest.raises(KeyError, match="'Missing' not found"):
            extract_definition(json_schema, "Missing")

    def test_key_error_lists_available(self):
        json_schema = self._make_schema({"Alpha": {}, "Beta": {}})
        with pytest.raises(KeyError, match="Alpha"):
            extract_definition(json_schema, "Missing")

    def test_refs_rewritten(self):
        json_schema = self._make_schema({
            "MyClass": {
                "type": "object",
                "properties": {"child": {"$ref": "#/$defs/Child"}},
            },
            "Child": {"type": "object"},
        })
        result = extract_definition(json_schema, "MyClass")
        assert result["properties"]["child"]["$ref"] == "#/components/schemas/Child"

    def test_template_prefix_stripped(self):
        json_schema = self._make_schema({
            "MyClass": {"type": "object", "description": "[TEMPLATE] A class"}
        })
        result = extract_definition(json_schema, "MyClass")
        assert result["description"] == "A class"

    def test_nullable_normalised(self):
        json_schema = self._make_schema({
            "MyClass": {
                "type": "object",
                "properties": {"name": {"type": ["string", "null"]}},
            }
        })
        result = extract_definition(json_schema, "MyClass")
        assert result["properties"]["name"]["nullable"] is True
        assert result["properties"]["name"]["type"] == "string"

    def test_ref_with_sibling_wrapped_in_allof(self):
        json_schema = self._make_schema({
            "MyClass": {
                "type": "object",
                "properties": {
                    "child": {"$ref": "#/$defs/Child", "description": "A child"}
                },
            },
            "Child": {"type": "object"},
        })
        result = extract_definition(json_schema, "MyClass")
        prop = result["properties"]["child"]
        assert "allOf" in prop
        assert prop["allOf"] == [{"$ref": "#/components/schemas/Child"}]
        assert prop["description"] == "A child"


# ─────────────────────────────────────────────────────────────────────────────
# collect_dependencies
# ─────────────────────────────────────────────────────────────────────────────

class TestCollectDependencies:
    def _make_schema(self, defs: dict) -> dict:
        return {"$defs": defs}

    def test_collects_direct_dependency(self):
        json_schema = self._make_schema({
            "Root": {
                "type": "object",
                "properties": {"child": {"$ref": "#/$defs/Child"}},
            },
            "Child": {"type": "object"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert "Child" in deps

    def test_collects_transitive_dependency(self):
        json_schema = self._make_schema({
            "Root": {
                "properties": {"a": {"$ref": "#/$defs/A"}},
            },
            "A": {
                "properties": {"b": {"$ref": "#/$defs/B"}},
            },
            "B": {"type": "string"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert "A" in deps
        assert "B" in deps

    def test_root_not_in_deps(self):
        json_schema = self._make_schema({
            "Root": {
                "properties": {"child": {"$ref": "#/$defs/Child"}},
            },
            "Child": {"type": "object"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert "Root" not in deps

    def test_no_deps_returns_empty(self):
        json_schema = self._make_schema({
            "Root": {"type": "string"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert deps == {}

    def test_circular_refs_handled(self):
        """Circular references must not cause infinite recursion."""
        json_schema = self._make_schema({
            "A": {"properties": {"b": {"$ref": "#/$defs/B"}}},
            "B": {"properties": {"a": {"$ref": "#/$defs/A"}}},
        })
        deps = collect_dependencies(json_schema, "A")
        assert "B" in deps

    def test_deps_have_refs_rewritten(self):
        json_schema = self._make_schema({
            "Root": {"properties": {"c": {"$ref": "#/$defs/Child"}}},
            "Child": {"properties": {"x": {"$ref": "#/$defs/GrandChild"}}},
            "GrandChild": {"type": "string"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert deps["Child"]["properties"]["x"]["$ref"] == "#/components/schemas/GrandChild"

    def test_deps_have_template_prefix_stripped(self):
        json_schema = self._make_schema({
            "Root": {"properties": {"c": {"$ref": "#/$defs/Child"}}},
            "Child": {"type": "object", "description": "[TEMPLATE] Child desc"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert deps["Child"]["description"] == "Child desc"

    def test_deps_have_nullable_normalised(self):
        json_schema = self._make_schema({
            "Root": {"properties": {"c": {"$ref": "#/$defs/Child"}}},
            "Child": {"type": ["string", "null"]},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert deps["Child"]["nullable"] is True
        assert deps["Child"]["type"] == "string"

    def test_missing_name_returns_empty(self):
        json_schema = self._make_schema({"Root": {"type": "object"}})
        deps = collect_dependencies(json_schema, "DoesNotExist")
        assert deps == {}

    def test_visited_prevents_duplicate_processing(self):
        """Shared dependency referenced by two parents is only collected once."""
        json_schema = self._make_schema({
            "Root": {
                "properties": {
                    "a": {"$ref": "#/$defs/A"},
                    "b": {"$ref": "#/$defs/B"},
                }
            },
            "A": {"properties": {"shared": {"$ref": "#/$defs/Shared"}}},
            "B": {"properties": {"shared": {"$ref": "#/$defs/Shared"}}},
            "Shared": {"type": "string"},
        })
        deps = collect_dependencies(json_schema, "Root")
        assert "Shared" in deps
        # Ensure it appears exactly once (dict key uniqueness guarantees this)
        assert list(deps.keys()).count("Shared") == 1


# ─────────────────────────────────────────────────────────────────────────────
# generate_json_schema (cache behaviour)
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateJsonSchema:
    def test_caches_result(self, tmp_path):
        """The same file must only be processed once."""
        fake_schema = {"$defs": {"Foo": {"type": "object"}}}

        with patch("src.converter.JsonSchemaGenerator") as MockGen:
            instance = MagicMock()
            instance.serialize.return_value = '{"$defs": {"Foo": {"type": "object"}}}'
            MockGen.return_value = instance

            import src.converter as conv
            conv._schema_cache.clear()

            linkml_file = tmp_path / "schema.yaml"
            linkml_file.write_text("# dummy")

            result1 = generate_json_schema(linkml_file)
            result2 = generate_json_schema(linkml_file)

            assert result1 == result2
            # Generator must only be instantiated once
            assert instance.serialize.call_count == 1

    def test_returns_parsed_dict(self, tmp_path):
        with patch("src.converter.JsonSchemaGenerator") as MockGen:
            instance = MagicMock()
            instance.serialize.return_value = '{"$defs": {}}'
            MockGen.return_value = instance

            import src.converter as conv
            conv._schema_cache.clear()

            linkml_file = tmp_path / "schema.yaml"
            linkml_file.write_text("# dummy")

            result = generate_json_schema(linkml_file)
            assert isinstance(result, dict)
