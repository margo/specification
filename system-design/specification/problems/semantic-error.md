# semantic-error

- Type URI: https://docs.margo.org/specification/problems/semantic-error
- HTTP status: 422 Unprocessable Content
- Summary: Request body includes a semantic error.

This problem type is used for semantically invalid payloads that pass syntactic validation but violate business rules or required invariant constraints in the resource model.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/semantic-error",
  "title": "Semantic Error",
  "status": 422,
  "detail": "The request body includes a semantic error.",
  "instance": "/api/v1/clients/example/capabilities/device-1"
}
```

## When it applies

This is returned for schema- or validation-level semantic issues, such as a request body that does not conform to required Margo relationships or domain invariants.
