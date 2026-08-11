# server-cannot-generate-response

- Type URI: https://docs.margo.org/specification/problems/server-cannot-generate-response
- HTTP status: 406 Not Acceptable
- Summary: Server cannot generate a response matching the Accept header.

This problem type is used when the server cannot produce a response in the format or representation requested by the client.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/server-cannot-generate-response",
  "title": "Server Cannot Generate Response",
  "status": 406,
  "detail": "The server cannot generate a response matching the Accept header.",
  "instance": "/api/v1/clients/example/deployments"
}
```

## When it applies

This is returned if the client requests a manifest or representation format that the server does not support or cannot generate for the given resources.
