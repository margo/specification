# certificate-not-trusted

- Type URI: https://docs.margo.org/specification/problems/certificate-not-trusted
- HTTP status: 403 Forbidden
- Summary: Client certificate is not trusted or has been revoked.

This problem type identifies requests whose certificate chain is not accepted by the server, or whose trust anchor is rejected or revoked.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/certificate-not-trusted",
  "title": "Certificate Not Trusted",
  "status": 403,
  "detail": "Client certificate is not trusted or has been revoked.",
  "instance": "/api/v1/onboarding"
}
```

## When it applies

This is returned when the presented client certificate is not trusted by the Workload Fleet Manager, or has been revoked or rejected by policy.
