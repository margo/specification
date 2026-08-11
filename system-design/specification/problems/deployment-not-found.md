# deployment-not-found

- Type URI: https://docs.margo.org/specification/problems/deployment-not-found
- HTTP status: 404 Not Found
- Summary: Deployment not found for the given digest.

This problem type identifies requests for deployment content that cannot be retrieved by the server for the requested deployment ID and digest.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/deployment-not-found",
  "title": "Deployment Not Found",
  "status": 404,
  "detail": "Deployment not found for the given digest.",
  "instance": "/api/v1/clients/example/deployments/app-42/sha256:abc123"
}
```

## When it applies

This is returned when a deployment URL points to a deployment resource that does not exist or cannot be served for the requested content-addressed digest.
