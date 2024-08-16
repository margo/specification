# Certificate API

In order to facilitate secure communication between the device's management client and workload orchestration web service the workload orchestration web service's root CA certificate must be downloaded using the Onboarding API's `certificate` endpoint.

### Route and HTTP Methods

```http
GET /onboarding/certificate
```

### Response Body

```json
{
    "certificate":"<base-64 encoded certificate text>"
}
```
