import pytest
from src.converter import convert_class, convert_enum

# ── anyOf ─────────────────────────────────────────────────────────────────────

ANYOF_SCHEMA = {
    "classes": {
        "FlexValue": {
            "description": "A value that can be string or integer.",
            "attributes": {
                "value": {
                    "any_of": [
                        {"range": "string"},
                        {"range": "integer"},
                    ]
                }
            },
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_anyof_no_range():
    result = convert_class("FlexValue", ANYOF_SCHEMA)
    value = result["properties"]["value"]
    assert "anyOf" in value
    types = [m.get("type") for m in value["anyOf"]]
    assert "string" in types
    assert "integer" in types


# ── anyOf with pattern constraints on members ─────────────────────────────────

ANYOF_PATTERN_SCHEMA = {
    "classes": {
        "Identifier": {
            "attributes": {
                "id": {
                    "range": "string",
                    "any_of": [
                        {"range": "string", "pattern": r"^uuid:.*"},
                        {"range": "string", "pattern": r"^urn:.*"},
                    ],
                }
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_range_plus_anyof_produces_allof():
    result = convert_class("Identifier", ANYOF_PATTERN_SCHEMA)
    id_prop = result["properties"]["id"]
    # range + any_of → allOf: [base, anyOf: [...]]
    assert "allOf" in id_prop
    members = id_prop["allOf"]
    assert any("type" in m and m["type"] == "string" for m in members)
    anyof_member = next(m for m in members if "anyOf" in m)
    patterns = [m.get("pattern") for m in anyof_member["anyOf"]]
    assert r"^uuid:.*" in patterns
    assert r"^urn:.*" in patterns


# ── allOf ─────────────────────────────────────────────────────────────────────

ALLOF_SCHEMA = {
    "classes": {
        "Base": {
            "attributes": {
                "id": {"range": "string", "required": True},
            }
        },
        "Extended": {
            "is_a": "Base",
            "attributes": {
                "extra": {"range": "string"},
            },
        },
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_is_a_produces_allof():
    result = convert_class("Extended", ALLOF_SCHEMA)
    assert "allOf" in result
    refs = [m.get("$ref") for m in result["allOf"] if "$ref" in m]
    assert "#/components/schemas/Base" in refs


def test_allof_child_has_own_properties():
    result = convert_class("Extended", ALLOF_SCHEMA)
    # The object schema with properties is one of the allOf members
    obj_member = next(
        m for m in result["allOf"]
        if m.get("type") == "object"
    )
    assert "extra" in obj_member["properties"]


# ── oneOf ─────────────────────────────────────────────────────────────────────

ONEOF_SCHEMA = {
    "classes": {
        "StrictChoice": {
            "attributes": {
                "mode": {
                    "exactly_one_of": [
                        {"range": "string"},
                        {"range": "integer"},
                    ]
                }
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_exactly_one_of_produces_oneof():
    result = convert_class("StrictChoice", ONEOF_SCHEMA)
    mode = result["properties"]["mode"]
    assert "oneOf" in mode
    types = [m.get("type") for m in mode["oneOf"]]
    assert "string" in types
    assert "integer" in types


# ── not ───────────────────────────────────────────────────────────────────────

NONEOF_SCHEMA = {
    "classes": {
        "Restricted": {
            "attributes": {
                "value": {
                    "range": "string",
                    "none_of": [
                        {"range": "integer"},
                    ],
                }
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_none_of_produces_not():
    result = convert_class("Restricted", NONEOF_SCHEMA)
    value = result["properties"]["value"]
    # range + none_of → allOf: [base, not: {...}]
    assert "allOf" in value
    not_member = next(m for m in value["allOf"] if "not" in m)
    assert not_member["not"]["type"] == "integer"


# ── Class-level anyOf ─────────────────────────────────────────────────────────

CLASS_LEVEL_ANYOF_SCHEMA = {
    "classes": {
        "Animal": {
            "attributes": {
                "name": {"range": "string", "required": True},
            }
        },
        "Dog": {
            "attributes": {
                "breed": {"range": "string"},
            }
        },
        "Cat": {
            "attributes": {
                "indoor": {"range": "boolean"},
            }
        },
        "Pet": {
            "description": "A pet that is either a Dog or a Cat.",
            "attributes": {
                "owner": {"range": "string", "required": True},
            },
            "any_of": [
                {"range": "Dog"},
                {"range": "Cat"},
            ],
        },
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_class_level_anyof():
    result = convert_class("Pet", CLASS_LEVEL_ANYOF_SCHEMA)
    assert "allOf" in result
    anyof_member = next(
        (m for m in result["allOf"] if "anyOf" in m), None
    )
    assert anyof_member is not None
    refs = [m.get("$ref") for m in anyof_member["anyOf"]]
    assert "#/components/schemas/Dog" in refs
    assert "#/components/schemas/Cat" in refs


# ── Multivalued anyOf ─────────────────────────────────────────────────────────

MULTIVALUED_ANYOF_SCHEMA = {
    "classes": {
        "Container": {
            "attributes": {
                "items": {
                    "multivalued": True,
                    "minimum_cardinality": 1,
                    "any_of": [
                        {"range": "string"},
                        {"range": "integer"},
                    ],
                }
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_multivalued_anyof():
    result = convert_class("Container", MULTIVALUED_ANYOF_SCHEMA)
    items_prop = result["properties"]["items"]
    assert items_prop["type"] == "array"
    assert items_prop["minItems"] == 1
    assert "anyOf" in items_prop["items"]
