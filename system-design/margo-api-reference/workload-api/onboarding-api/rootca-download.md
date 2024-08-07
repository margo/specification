# Download Root CA Certificate

In order to facilitate secure communication between the management client and workload orchestration web service the workload orchestration web service's root CA certificate must be downloaded using the Onboarding API.

### Route and HTTP Methods

```http
GET /onboarding/certificate
```

### Response Body

```json
{
    "certificate":"<certificate text>"
}
```
