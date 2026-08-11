# invalid-certificate-format

- Type URI: https://docs.margo.org/specification/problems/invalid-certificate-format
- HTTP status: 400 Bad Request
- Summary: Invalid certificate format or structure.

This problem type is used when a client certificate cannot be parsed, is structurally invalid, or does not satisfy the expected X.509 requirements for onboarding or signed requests.

## Example problem response

```json
{
  "type": "https://docs.margo.org/specification/problems/invalid-certificate-format",
  "title": "Invalid Certificate",
  "status": 400,
  "detail": "Certificate format is invalid or structure is malformed.",
  "instance": "/api/v1/onboarding"
}
```

## When it applies

This condition is returned when the request includes a certificate payload that is missing required fields, malformed, or not acceptable for the expected certificate validation flow.
