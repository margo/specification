# Deployment Status

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


## Request Body Attributes

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version the API resource follows.|
| kind            | string    | Y    | Must be `DeploymentStatusManifest`.|
| deploymentId    | string    | Y    | The unique identifier UUID of the deployment specification. Needs to be assigned by the Workload Fleet Management Software. |
| status          | []status    | Y    | Element that defines overall deployment status. See the [Status Attributes](#status-attributes) section below.|
| components      | []components    | Y    | Element that defines the individual component's deployment status. See the [Component Attributes](#component-attributes) section below.|

#### Status Attributes

| Fields      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| state      | string    | Y    | Current state of the overall deployment. The state value MUST be one the following options: pending, installing, installed, removing, removed, failed. The overall deployment status MUST reflect the most severe of the components states, following this precedence: failed > removing > installing > pending > removing > installed.|
| error      | Error    | N    | Element that defines the overall installation error if one occured. See the [Error Attributes](#error-attributes) section below.|

#### Component Attributes

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the deployment component, inherited via the deployment specification |
| state     | string    | Y    | The component's current deployment state of the component. MUST be one of the following options: pending, installing, installed, removing, removed, failed |
| error     | Error    | N    | Element that defines the components installation error if one occured. See the [Error Attributes](#error-attributes) section below.  |

> Note: The components array MUST contain one entry for each "component" defined in the referenced ApplicationDeployment manifest. 

#### Error Attributes

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| code      | string    | Y    | Associated error code following a component failure during installation. |
| message   | string    | Y    | Associated error message that provides further details to the WFM about the error that was encountered. |

> Note: Error codes and messages are implementation-specific. 

## Example Deployment Status Manifest Request

```json
{
    "apiVersion": "deployment.margo.org/v1alpha1",
    "kind": "DeploymentStatusManifest",
    "deploymentId": "a3e2f5dc-912e-494f-8395-52cf3769bc06",
    "status": {
        "state": "pending",
        "error": {
            "code": "",
            "message": ""
        }
    },
    "components": [
        {
            "name": "digitron-orchestrator",
            "state": "pending",
            "error": {
                "code":"",
                "message":""
            }
        },
        {
            "name": "database-services",
            "state": "pending",
            "error": {
                "code": "",
                "message": ""
            }
        }
    ]
}
```