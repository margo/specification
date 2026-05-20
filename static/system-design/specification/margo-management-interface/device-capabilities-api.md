# Device Capabilities API

Devices MUST provide the Workload Fleet Management service with its capabilities and characteristics. This is done by calling the Device API's `device capabilities` endpoint. Reporting the device capabilities is the final step in the onboarding of the device's client. 

To ensure the WFM is kept up to date, the device's client MUST send updated capabilities information if any changes occur to the information originally provided (i.e., additional memory is added to the device).

- Requests to this endpoint MUST be authenticated using the HTTP Message Signature method as defined in the [Payload Security](../margo-management-interface/api-requirements-and-security.md#payload-security-method) section.

## Route and HTTP Methods

```https
POST /api/v1/clients/{clientId}/capabilities
PUT /api/v1/clients/{clientId}/capabilities
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {clientId} | string | Y | The unique identifier of the (device) client registered with the WFM during onboarding. |

### Response Codes

| Code | Description |
|------|-------------|
| 201 OK | The device capabilities document was added, or updated, successfully |
| 400 Bad Request | Missing or invalid content-digest header. Ensure the SHA256 hash of the base64-encoded payload is included. |
| 401 Unauthorized | Signature verification failed. Ensure you are signing with the correct X.509 private key.  |
| 403 Forbidden | Client certificate is not trusted or has been revoked. |
| 422 Unprocessable Content | Request body includes a semantic error.  |

## Request Body

[DeviceCapabilitiesManifest](./device-capabilities.md) document describing a device's capabilities and characteristics.

