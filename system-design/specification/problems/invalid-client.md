# invalid-client

- Type URI: https://docs.margo.org/specification/problems/invalid-client
- HTTP status: 404 Not Found
- Summary: No client with the given client ID was found.

This problem type indicates that the server cannot find a client identified by the request path or request context.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/invalid-client",
  "title": "Invalid Client",
  "status": 404,
  "detail": "No client with the given client ID was found.",
  "instance": "/api/v1/clients/unknown/deployments"
}
```

## When it applies

This is returned when a request references an unknown or unregistered client ID.
