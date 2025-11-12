# Certificate API

In order to facilitate secure communication between the device's management client and the Workload Fleet Manager, the device must first retrieve the root CA certificate  using the Onboarding API's `certificate` endpoint.

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
