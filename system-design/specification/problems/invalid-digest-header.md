# invalid-digest-header

- Type URI: https://docs.margo.org/specification/problems/invalid-digest-header
- HTTP status: 400 Bad Request
- Summary: Missing or invalid content-digest header. Ensure the SHA256 hash of the payload is included.

This problem type identifies requests that do not include a valid `Content-Digest` header or include a digest that does not validate against the request payload.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/invalid-digest-header",
  "title": "Invalid Digest Header",
  "status": 400,
  "detail": "Missing or invalid content-digest header. Ensure the SHA256 hash of the payload is included.",
  "instance": "/api/v1/clients/example/capabilities/device-1"
}
```

## When it applies

This condition is returned when the payload signature process expects a valid SHA-256 digest and the message does not include or cannot verify the required digest.
