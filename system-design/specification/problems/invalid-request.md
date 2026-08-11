# invalid-request

- Type URI: https://docs.margo.org/specification/problems/invalid-request
- HTTP status: 400 Bad Request
- Summary: Invalid request.

This problem type indicates that the server rejected the request because the request shape, encoding, or parameter semantics were invalid.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/invalid-request",
  "title": "Invalid Request",
  "status": 400,
  "detail": "The request could not be processed because it was malformed or invalid.",
  "instance": "/api/v1/clients/example/bundles"
}
```

## When it applies

This is used for syntactically invalid HTTP requests or malformed resource references that are not covered by a more specific Margo type URI.
