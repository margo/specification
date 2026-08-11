# invalid-bundle

- Type URI: https://docs.margo.org/specification/problems/invalid-bundle
- HTTP status: 404 Not Found
- Summary: Bundle not found for the given digest.

This problem type is returned when the referenced bundle archive cannot be served for the provided digest.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/invalid-bundle",
  "title": "Invalid Bundle",
  "status": 404,
  "detail": "Bundle not found for the given digest.",
  "instance": "/api/v1/clients/example/bundles/sha256:abc123"
}
```

## When it applies

This is used when a bundle URL or digest cannot be resolved to an immutable bundle archive that matches the requested content address.
