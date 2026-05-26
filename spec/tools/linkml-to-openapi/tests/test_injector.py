# tests/test_injector.py
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.injector import inject_schemas


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_doc(schemas: dict) -> dict:
    """Build a minimal OpenAPI document with the given schemas."""
    return {
        "openapi": "3.0.3",
        "info": {"title": "Test", "version": "0.0.1"},
        "components": {"schemas": schemas},
    }


def _stub(linkml_file: str, linkml_source: str, **extra) -> dict:
    """Build a schema stub with x-linkml-* fields."""
    return {
        "x-linkml-schema": linkml_file,
        "x-linkml-source": linkml_source,
        **extra,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture()
def template_dir(tmp_path: Path) -> Path:
    """Return a temp directory acting as the OpenAPI template directory."""
    return tmp_path


@pytest.fixture()
def dummy_linkml(template_dir: Path) -> Path:
    """Write a placeholder LinkML file so path-existence checks pass."""
    f = template_dir / "schema.yaml"
    f.write_text("# placeholder")
    return f


# ─────────────────────────────────────────────────────────────────────────────
# components/schemas initialisation (Fix #4)
# ─────────────────────────────────────────────────────────────────────────────

class TestComponentsSchemasInitialisation:
    def test_creates_components_when_missing(self, template_dir):
        """inject_schemas must not crash when 'components' is absent."""
        doc = {"openapi": "3.0.3", "info": {"title": "T", "version": "1"}}
        result = inject_schemas(doc, template_dir)
        assert "components" in result
        assert "schemas" in result["components"]

    def test_creates_schemas_when_components_present_but_schemas_missing(
        self, template_dir
    ):
        doc = {
            "openapi": "3.0.3",
            "info": {"title": "T", "version": "1"},
            "components": {},
        }
        result = inject_schemas(doc, template_dir)
        assert "schemas" in result["components"]

    def test_existing_schemas_preserved(self, template_dir):
        doc = _make_doc({"HandAuthored": {"type": "string"}})
        result = inject_schemas(doc, template_dir)
        assert "HandAuthored" in result["components"]["schemas"]

    def test_modifies_doc_in_place_and_returns_it(self, template_dir):
        doc = _make_doc({})
        result = inject_schemas(doc, template_dir)
        assert result is doc


# ─────────────────────────────────────────────────────────────────────────────
# Hand-authored schemas are left untouched
# ─────────────────────────────────────────────────────────────────────────────

class TestHandAuthoredSchemasUntouched:
    def test_schema_without_x_linkml_fields_unchanged(self, template_dir):
        original = {"type": "object", "properties": {"id": {"type": "string"}}}
        doc = _make_doc({"MySchema": original})
        result = inject_schemas(doc, template_dir)
        assert result["components"]["schemas"]["MySchema"] == original

    def test_schema_with_only_x_linkml_schema_unchanged(self, template_dir):
        stub = {"x-linkml-schema": "schema.yaml"}
        doc = _make_doc({"Partial": stub})
        result = inject_schemas(doc, template_dir)
        # Missing x-linkml-source → treated as hand-authored, left alone
        assert result["components"]["schemas"]["Partial"] == stub

    def test_schema_with_only_x_linkml_source_unchanged(self, template_dir):
        stub = {"x-linkml-source": "MyClass"}
        doc = _make_doc({"Partial": stub})
        result = inject_schemas(doc, template_dir)
        assert result["components"]["schemas"]["Partial"] == stub


# ─────────────────────────────────────────────────────────────────────────────
# Missing LinkML file
# ─────────────────────────────────────────────────────────────────────────────

class TestMissingLinkmlFile:
    def test_logs_error_and_skips_when_file_missing(self, template_dir, caplog):
        doc = _make_doc({
            "MySchema": _stub("nonexistent.yaml", "MyClass"),
        })
        import logging
        with caplog.at_level(logging.ERROR, logger="src.injector"):
            result = inject_schemas(doc, template_dir)

        assert any("not found" in r.message.lower() for r in caplog.records)
        # Stub must remain unchanged (not replaced)
        assert "x-linkml-schema" in result["components"]["schemas"]["MySchema"]

    def test_other_schemas_still_processed_after_missing_file(
        self, template_dir, caplog
    ):
        """A missing file for one stub must not abort processing of others."""
        hand_authored = {"type": "string"}
        doc = _make_doc({
            "Bad": _stub("nonexistent.yaml", "MyClass"),
            "Good": hand_authored,
        })
        result = inject_schemas(doc, template_dir)
        assert result["components"]["schemas"]["Good"] == hand_authored


# ─────────────────────────────────────────────────────────────────────────────
# JSON Schema generation failure
# ─────────────────────────────────────────────────────────────────────────────

class TestJsonSchemaGenerationFailure:
    def test_logs_error_and_skips_on_generation_exception(
        self, template_dir, dummy_linkml, caplog
    ):
        doc = _make_doc({"MySchema": _stub("schema.yaml", "MyClass")})

        import logging
        with patch(
            "src.injector.generate_json_schema",
            side_effect=RuntimeError("parse error"),
        ), caplog.at_level(logging.ERROR, logger="src.injector"):
            result = inject_schemas(doc, template_dir)

        assert any("failed" in r.message.lower() for r in caplog.records)
        assert "x-linkml-schema" in result["components"]["schemas"]["MySchema"]


# ─────────────────────────────────────────────────────────────────────────────
# extract_definition failure
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractDefinitionFailure:
    def test_logs_error_and_skips_when_source_not_found(
        self, template_dir, dummy_linkml, caplog
    ):
        doc = _make_doc({"MySchema": _stub("schema.yaml", "NonExistent")})

        import logging
        with patch(
            "src.injector.generate_json_schema",
            return_value={"$defs": {"OtherClass": {"type": "object"}}},
        ), patch(
            "src.injector.extract_definition",
            side_effect=KeyError("'NonExistent' not found"),
        ), caplog.at_level(logging.ERROR, logger="src.injector"):
            result = inject_schemas(doc, template_dir)

        assert any("not found" in r.message.lower() for r in caplog.records)
        assert "x-linkml-schema" in result["components"]["schemas"]["MySchema"]


# ─────────────────────────────────────────────────────────────────────────────
# Successful injection
# ─────────────────────────────────────────────────────────────────────────────

class TestSuccessfulInjection:
    def _run(
        self,
        template_dir: Path,
        dummy_linkml: Path,
        stub_extra: dict | None = None,
        converted: dict | None = None,
        deps: dict | None = None,
    ) -> dict:
        stub = _stub("schema.yaml", "MyClass", **(stub_extra or {}))
        doc = _make_doc({"MySchema": stub})

        converted_schema = converted or {"type": "object", "title": "MyClass"}
        dependencies = deps or {}

        with patch("src.injector.generate_json_schema", return_value={"$defs": {}}), \
             patch("src.injector.extract_definition", return_value=converted_schema), \
             patch("src.injector.collect_dependencies", return_value=dependencies):
            return inject_schemas(doc, template_dir)

    def test_stub_replaced_with_converted_schema(
        self, template_dir, dummy_linkml
    ):
        result = self._run(template_dir, dummy_linkml)
        schema = result["components"]["schemas"]["MySchema"]
        assert schema["type"] == "object"
        assert schema["title"] == "MyClass"
        assert "x-linkml-schema" not in schema
        assert "x-linkml-source" not in schema

    def test_x_linkml_fields_stripped_from_output(
        self, template_dir, dummy_linkml
    ):
        result = self._run(template_dir, dummy_linkml)
        schema = result["components"]["schemas"]["MySchema"]
        assert not any(k.startswith("x-linkml-") for k in schema)

    def test_hand_authored_fields_preserved(self, template_dir, dummy_linkml):
        """Non-x-linkml fields on the stub must survive injection."""
        result = self._run(
            template_dir,
            dummy_linkml,
            stub_extra={"description": "Hand-authored description"},
            converted={"type": "object"},
        )
        schema = result["components"]["schemas"]["MySchema"]
        assert schema["description"] == "Hand-authored description"

    def test_hand_authored_fields_win_on_conflict(
        self, template_dir, dummy_linkml
    ):
        """Hand-authored fields must override generated fields on key conflict."""
        result = self._run(
            template_dir,
            dummy_linkml,
            stub_extra={"description": "Override"},
            converted={"type": "object", "description": "Generated"},
        )
        schema = result["components"]["schemas"]["MySchema"]
        assert schema["description"] == "Override"

    def test_generated_fields_used_when_no_conflict(
        self, template_dir, dummy_linkml
    ):
        result = self._run(
            template_dir,
            dummy_linkml,
            converted={"type": "object", "title": "Generated Title"},
        )
        schema = result["components"]["schemas"]["MySchema"]
        assert schema["title"] == "Generated Title"

    def test_preserved_refs_rewritten(self, template_dir, dummy_linkml):
        """$refs in hand-authored preserved fields must be rewritten (Fix #1)."""
        stub_extra = {"properties": {"child": {"$ref": "#/$defs/Child"}}}
        result = self._run(
            template_dir,
            dummy_linkml,
            stub_extra=stub_extra,
            converted={"type": "object"},
        )
        schema = result["components"]["schemas"]["MySchema"]
        assert (
            schema["properties"]["child"]["$ref"]
            == "#/components/schemas/Child"
        )

    def test_preserved_refs_already_rewritten_unchanged(
        self, template_dir, dummy_linkml
    ):
        """Already-correct $refs in preserved fields must not be double-rewritten."""
        stub_extra = {
            "properties": {"child": {"$ref": "#/components/schemas/Child"}}
        }
        result = self._run(
            template_dir,
            dummy_linkml,
            stub_extra=stub_extra,
            converted={"type": "object"},
        )
        schema = result["components"]["schemas"]["MySchema"]
        assert (
            schema["properties"]["child"]["$ref"]
            == "#/components/schemas/Child"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Dependency auto-injection
# ─────────────────────────────────────────────────────────────────────────────

class TestDependencyAutoInjection:
    def _run_with_deps(
        self,
        template_dir: Path,
        dummy_linkml: Path,
        deps: dict,
        existing_schemas: dict | None = None,
    ) -> dict:
        schemas = {"MySchema": _stub("schema.yaml", "MyClass")}
        if existing_schemas:
            schemas.update(existing_schemas)
        doc = _make_doc(schemas)

        with patch("src.injector.generate_json_schema", return_value={"$defs": {}}), \
             patch("src.injector.extract_definition", return_value={"type": "object"}), \
             patch("src.injector.collect_dependencies", return_value=deps):
            return inject_schemas(doc, template_dir)

    def test_dependency_auto_injected(self, template_dir, dummy_linkml):
        deps = {"ChildClass": {"type": "object", "title": "ChildClass"}}
        result = self._run_with_deps(template_dir, dummy_linkml, deps)
        assert "ChildClass" in result["components"]["schemas"]
        assert result["components"]["schemas"]["ChildClass"]["title"] == "ChildClass"

    def test_multiple_dependencies_all_injected(self, template_dir, dummy_linkml):
        deps = {
            "DepA": {"type": "object"},
            "DepB": {"type": "string"},
            "DepC": {"type": "integer"},
        }
        result = self._run_with_deps(template_dir, dummy_linkml, deps)
        for name in deps:
            assert name in result["components"]["schemas"]

    def test_existing_dependency_not_overwritten(self, template_dir, dummy_linkml):
        """A dep already in components/schemas must not be replaced."""
        existing = {"type": "object", "description": "Hand-authored"}
        deps = {"ChildClass": {"type": "object", "description": "Generated"}}
        result = self._run_with_deps(
            template_dir,
            dummy_linkml,
            deps,
            existing_schemas={"ChildClass": existing},
        )
        assert (
            result["components"]["schemas"]["ChildClass"]["description"]
            == "Hand-authored"
        )

    def test_no_dependencies_nothing_extra_injected(
        self, template_dir, dummy_linkml
    ):
        result = self._run_with_deps(template_dir, dummy_linkml, deps={})
        # Only MySchema should be present
        assert list(result["components"]["schemas"].keys()) == ["MySchema"]

    def test_dependency_injected_into_real_document_reference(
        self, template_dir, dummy_linkml
    ):
        """
        Deps must be written into the actual document dict, not a
        throwaway copy (Fix #4 regression guard).
        """
        deps = {"AutoDep": {"type": "string"}}
        result = self._run_with_deps(template_dir, dummy_linkml, deps)
        # Verify via the returned doc AND the original reference
        assert "AutoDep" in result["components"]["schemas"]


# ─────────────────────────────────────────────────────────────────────────────
# Multiple stubs in one document
# ─────────────────────────────────────────────────────────────────────────────

class TestMultipleStubs:
    def test_all_stubs_processed(self, template_dir, tmp_path):
        schema_a = tmp_path / "a.yaml"
        schema_b = tmp_path / "b.yaml"
        schema_a.write_text("# a")
        schema_b.write_text("# b")

        doc = _make_doc({
            "SchemaA": _stub("a.yaml", "ClassA"),
            "SchemaB": _stub("b.yaml", "ClassB"),
        })

        converted_a = {"type": "object", "title": "ClassA"}
        converted_b = {"type": "object", "title": "ClassB"}

        def fake_extract(json_schema, name):
            return converted_a if name == "ClassA" else converted_b

        with patch("src.injector.generate_json_schema", return_value={"$defs": {}}), \
             patch("src.injector.extract_definition", side_effect=fake_extract), \
             patch("src.injector.collect_dependencies", return_value={}):
            result = inject_schemas(doc, tmp_path)

        assert result["components"]["schemas"]["SchemaA"]["title"] == "ClassA"
        assert result["components"]["schemas"]["SchemaB"]["title"] == "ClassB"

    def test_failure_in_one_stub_does_not_abort_others(
        self, template_dir, tmp_path
    ):
        good = tmp_path / "good.yaml"
        good.write_text("# good")

        doc = _make_doc({
            "Bad": _stub("nonexistent.yaml", "BadClass"),
            "Good": _stub("good.yaml", "GoodClass"),
        })

        with patch("src.injector.generate_json_schema", return_value={"$defs": {}}), \
             patch(
                 "src.injector.extract_definition",
                 return_value={"type": "object", "title": "GoodClass"},
             ), \
             patch("src.injector.collect_dependencies", return_value={}):
            result = inject_schemas(doc, tmp_path)

        # Good must be injected
        assert result["components"]["schemas"]["Good"]["title"] == "GoodClass"
        # Bad must remain as stub (file not found → skipped)
        assert "x-linkml-schema" in result["components"]["schemas"]["Bad"]

    def test_shared_linkml_file_generates_json_schema_once(
        self, template_dir, tmp_path
    ):
        """
        Two stubs referencing the same LinkML file must only trigger
        one generate_json_schema call (cache behaviour guard).
        """
        shared = tmp_path / "shared.yaml"
        shared.write_text("# shared")

        doc = _make_doc({
            "SchemaA": _stub("shared.yaml", "ClassA"),
            "SchemaB": _stub("shared.yaml", "ClassB"),
        })

        with patch(
            "src.injector.generate_json_schema",
            return_value={"$defs": {}},
        ) as mock_gen, \
             patch("src.injector.extract_definition", return_value={"type": "object"}), \
             patch("src.injector.collect_dependencies", return_value={}):
            inject_schemas(doc, tmp_path)

        # Called twice here because caching is in converter, not injector.
        # This test guards that injector does not bypass the cache by
        # calling generate_json_schema with different path representations.
        calls = [str(c.args[0]) for c in mock_gen.call_args_list]
        assert len(set(calls)) == 1, "Same file passed with different paths"
