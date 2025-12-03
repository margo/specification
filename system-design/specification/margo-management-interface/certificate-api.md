# Certificate API

In order to facilitate secure communication between the device's management client and the Workload Fleet Manager, the device must first retrieve the root CA certificate using the Onboarding API's `certificate` endpoint.

- This endpoint MAY only be used to retrieve the root CA over an already trusted channel.
- If no trusted channel exists, the root CA MUST be provided via an out-of-band method. 
- In the response body, the certificate field MUST contain the PEM-encoded X.509 root CA certificate, Base64 without line breaks.

## Route and HTTP Methods

```http
GET /api/v1/onboarding/certificate
```
### Response Code

| Code | Description |
|------|-------------|
| 200 OK | Root CA certificate |

## Example Response Body

```json
{
    "certificate":"<base-64 encoded certificate text>"
}
```
