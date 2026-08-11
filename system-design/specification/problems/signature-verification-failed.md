# signature-verification-failed

- Type URI: https://docs.margo.org/specification/problems/signature-verification-failed
- HTTP status: 401 Unauthorized
- Summary: Signature verification failed. Ensure you are signing with the correct X.509 private key.

This problem type is used when the server cannot verify the payload signature for a request.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/signature-verification-failed",
  "title": "Signature Verification Failed",
  "status": 401,
  "detail": "Signature verification failed. Ensure you are signing with the correct X.509 private key.",
  "instance": "/api/v1/clients/example/deployments"
}
```

## When it applies

This condition is returned when the request includes a signature that does not match the payload or the certificate used to verify the signature does not correspond to the expected client identity.
