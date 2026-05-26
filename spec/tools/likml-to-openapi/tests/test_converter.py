import pytest
from src.converter import convert_class, convert_enum

# ── Existing fixtures (unchanged) ─────────────────────────────────────────────

SIMPLE_SCHEMA = {
    "classes": {
        "OnboardingRequest": {
            "description": "Onboarding manifest.",
            "attributes": {
                "apiVersion": {"range": "string", "required": True},
                "kind": {"equals_string": "OnboardingRequest", "required": True},
                "certificate": {"range": "string", "required": True},
            },
        }
    },
    "enums": {
        "DeviceRole": {
            "description": "Device roles.",
            "permissible_values": {
                "Standalone Cluster": {},
                "Standalone Device": {},
                "Cluster Leader": {},
            },
        }
    },
    "types": {},
    "slots": {},
}


def test_convert_enum():
    result = convert_enum("DeviceRole", SIMPLE_SCHEMA)
    assert result["type"] == "string"
    assert "Standalone Cluster" in result["enum"]
    assert len(result["enum"]) == 3


def test_convert_class_required_fields():
    result = convert_class("OnboardingRequest", SIMPLE_SCHEMA)
    assert set(result["required"]) == {"apiVersion", "kind", "certificate"}


def test_convert_class_equals_string():
    result = convert_class("OnboardingRequest", SIMPLE_SCHEMA)
    kind_prop = result["properties"]["kind"]
    assert kind_prop["type"] == "string"
    assert kind_prop["enum"] == ["OnboardingRequest"]


# ── Pattern constraints ───────────────────────────────────────────────────────

PATTERN_SCHEMA = {
    "classes": {
        "Device": {
            "attributes": {
                "serialNumber": {
                    "range": "string",
                    "required": True,
                    "pattern": r"^[A-Z0-9\-]{6,20}$",
                },
                "firmwareVersion": {
                    "range": "string",
                    "pattern": r"^\d+\.\d+\.\d+$",
                    "min_length": 5,
                    "max_length": 20,
                },
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_pattern_applied_to_string():
    result = convert_class("Device", PATTERN_SCHEMA)
    serial = result["properties"]["serialNumber"]
    assert serial["type"] == "string"
    assert serial["pattern"] == r"^[A-Z0-9\-]{6,20}$"


def test_min_max_length_applied():
    result = convert_class("Device", PATTERN_SCHEMA)
    fw = result["properties"]["firmwareVersion"]
    assert fw["minLength"] == 5
    assert fw["maxLength"] == 20
    assert fw["pattern"] == r"^\d+\.\d+\.\d+$"


# ── Numeric range constraints ─────────────────────────────────────────────────

NUMERIC_SCHEMA = {
    "classes": {
        "Resources": {
            "attributes": {
                "cpuCount": {
                    "range": "integer",
                    "required": True,
                    "minimum_value": 1,
                    "maximum_value": 256,
                },
                "memoryGiB": {
                    "range": "float",
                    "minimum_value": 0.5,
                    "exclusive_maximum_value": 1024.0,
                },
                "loadFactor": {
                    "range": "double",
                    "exclusive_minimum_value": 0.0,
                    "exclusive_maximum_value": 1.0,
                },
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_integer_min_max():
    result = convert_class("Resources", NUMERIC_SCHEMA)
    cpu = result["properties"]["cpuCount"]
    assert cpu["type"] == "integer"
    assert cpu["minimum"] == 1
    assert cpu["maximum"] == 256


def test_float_exclusive_maximum():
    result = convert_class("Resources", NUMERIC_SCHEMA)
    mem = result["properties"]["memoryGiB"]
    assert mem["minimum"] == 0.5
    assert mem["exclusiveMaximum"] == 1024.0
    assert "maximum" not in mem


def test_double_exclusive_min_max():
    result = convert_class("Resources", NUMERIC_SCHEMA)
    lf = result["properties"]["loadFactor"]
    assert lf["exclusiveMinimum"] == 0.0
    assert lf["exclusiveMaximum"] == 1.0


# ── Array cardinality constraints ─────────────────────────────────────────────

CARDINALITY_SCHEMA = {
    "classes": {
        "Device": {
            "attributes": {
                "roles": {
                    "range": "DeviceRole",
                    "multivalued": True,
                    "required": True,
                    "minimum_cardinality": 1,
                    "maximum_cardinality": 3,
                },
                "tags": {
                    "range": "string",
                    "multivalued": True,
                    "exact_cardinality": 2,
                },
            }
        }
    },
    "enums": {
        "DeviceRole": {
            "permissible_values": {
                "Standalone Cluster": {},
                "Standalone Device": {},
            }
        }
    },
    "types": {},
    "slots": {},
}


def test_array_min_max_items():
    result = convert_class("Device", CARDINALITY_SCHEMA)
    roles = result["properties"]["roles"]
    assert roles["type"] == "array"
    assert roles["minItems"] == 1
    assert roles["maxItems"] == 3


def test_exact_cardinality_sets_both():
    result = convert_class("Device", CARDINALITY_SCHEMA)
    tags = result["properties"]["tags"]
    assert tags["minItems"] == 2
    assert tags["maxItems"] == 2


# ── Constraints on multivalued scalars ────────────────────────────────────────

MULTIVALUED_SCALAR_SCHEMA = {
    "classes": {
        "Config": {
            "attributes": {
                "allowedPorts": {
                    "range": "integer",
                    "multivalued": True,
                    "minimum_value": 1,
                    "maximum_value": 65535,
                    "minimum_cardinality": 1,
                },
            }
        }
    },
    "enums": {},
    "types": {},
    "slots": {},
}


def test_multivalued_scalar_constraints():
    result = convert_class("Config", MULTIVALUED_SCALAR_SCHEMA)
    ports = result["properties"]["allowedPorts"]
    assert ports["type"] == "array"
    assert ports["minItems"] == 1
    # Numeric constraints live on items
    assert ports["items"]["minimum"] == 1
    assert ports["items"]["maximum"] == 65535
