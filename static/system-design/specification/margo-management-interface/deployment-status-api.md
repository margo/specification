# Deployment Status API

While applying a new desired state, the device's management client MUST provide the Workload Fleet Manager service with an indication of the current workload deployment status. This is done by calling the Device API's `deployment status` endpoint.

- Requests to this endpoint MUST be authenticated using the HTTP Message Signature method as defined in the [Payload Security](../margo-management-interface/api-requirements-and-security.md#payload-security-method) section.

> Note: This assumes consistent connection to the WFM, we will address intermittent or extended disconnection scenarios in the future. 

## Route and HTTP Methods

```https
POST /api/v1/clients/{clientId}/deployments/{deploymentId}/status
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {clientId} | string | Y | The unique identifier of the (device) client registered with the WFM during onboarding. |
| {deploymentId} | string | Y | The UUID of the `ApplicationDeployment` YAML being reported.

### Response Codes

| Code | Description |
|------|-------------|
| 200 OK  | The deployment status was added, or updated, successfully. |
| 400 Bad Request | Missing or invalid content-digest header. Ensure the SHA256 hash of the base64-encoded payload is included. |
| 401 Unauthorized | Signature verification failed. Ensure you are signing with the correct X.509 private key.  |
| 403 Forbidden | Client certificate is not trusted or has been revoked. |
| 422 Unprocessable Content | Request body includes a semantic error.  |


## Request Body

[DeploymentStatus](./deployment status.md) document describing the status of an application deployment.

