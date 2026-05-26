# Maps LinkML built-in types to OpenAPI/JSON Schema primitives
LINKML_TYPE_MAP: dict[str, dict] = {
    "string":     {"type": "string"},
    "integer":    {"type": "integer"},
    "float":      {"type": "number", "format": "float"},
    "double":     {"type": "number", "format": "double"},
    "boolean":    {"type": "boolean"},
    "date":       {"type": "string", "format": "date"},
    "datetime":   {"type": "string", "format": "date-time"},
    "uri":        {"type": "string", "format": "uri"},
    "uriorcurie": {"type": "string"},
    "curie":      {"type": "string"},
    "ncname":     {"type": "string"},
}

XSD_TYPE_MAP: dict[str, dict] = {
    "xsd:string":   {"type": "string"},
    "xsd:integer":  {"type": "integer"},
    "xsd:boolean":  {"type": "boolean"},
    "xsd:float":    {"type": "number", "format": "float"},
    "xsd:double":   {"type": "number", "format": "double"},
    "xsd:date":     {"type": "string", "format": "date"},
    "xsd:dateTime": {"type": "string", "format": "date-time"},
    "xsd:anyURI":   {"type": "string", "format": "uri"},
}

# LinkML attribute constraint keys that map to OpenAPI/JSON Schema keywords
# Format: { linkml_key: openapi_key }
NUMERIC_CONSTRAINT_MAP: dict[str, str] = {
    "minimum_value":          "minimum",
    "maximum_value":          "maximum",
    "exclusive_minimum_value": "exclusiveMinimum",
    "exclusive_maximum_value": "exclusiveMaximum",
}

STRING_CONSTRAINT_MAP: dict[str, str] = {
    "pattern":    "pattern",   # LinkML uses 'pattern' directly
    "min_length": "minLength",
    "max_length": "maxLength",
}

ARRAY_CONSTRAINT_MAP: dict[str, str] = {
    "minimum_cardinality": "minItems",
    "maximum_cardinality": "maxItems",
    "exact_cardinality":   None,   # handled specially → minItems + maxItems
}

# LinkML keys that map to OpenAPI composition keywords
COMPOSITION_MAP: dict[str, str] = {
    "any_of":   "anyOf",   # LinkML: any_of → OpenAPI: anyOf
    "all_of":   "allOf",   # LinkML: all_of → OpenAPI: allOf
    "exactly_one_of": "oneOf",  # LinkML: exactly_one_of → OpenAPI: oneOf
    "none_of":  "not",     # LinkML: none_of → OpenAPI: not (single schema)
}