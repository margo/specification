# Deployment Status

While applying a new desired state the device's management client MUST provide the workload orchestration web service with an indication of the current status. This is done calling the Device API's `device status` endpoint.

### Route and HTTP Methods

```http
POST /device/{deviceId}/deployment/{deploymentId}/status
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {deviceId} | string | Y | The device's Id registered with the workload orchestration solution during onboarding.|
| {deploymentId} | string | Y | The deployment Id the status is being reported for |

### Request Body Fields

> Action: Need to figure out the options for error code and message. Are these to be free form?

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `DeploymentStatus`.|
| deploymentId    | string    | Y    | The unique identifier UUID of the deployment specification. Needs to be assigned by the Workload Orchestration Software. |
| status          | []status    | Y    | Element that defines overall deployment status. See the [Status Fields](#status-fields) section below.|
| components      | []components    | Y    | Element that defines the individual component's deployment status. See the [Component Fields](#component-fields) section below.|

#### Status Fields

| Fields      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| state      | string    | Y    | Current state of the overall deployment. The state value MUST be one the following options: Pending, Installing, Installed, Failed. The overall deployment status MUST inherit the current component's status until it has gone through installing each component.|
| error      | Error    | N    | Element that defines the overall installation error if one occured. See the [Error Fields](#error-fields) section below.|

#### Component Fields

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the deployment component, inherited via the deployment specification |
| state     | string    | Y    | The component's current deployment state of the component. MUST be one of the following options: Pending, Installing, Installed, Failed |
| error     | Error    | N    | Element that defines the components installation error if one occured. See the [Error Fields](#error-fields) section below.  |

#### Error Fields

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| code      | string    | Y    | Associated error code following a component failure during installation. |
| message   | string    | Y    | Associated error message that provides further details to the WOS about the error that was encountered. |

### Example Request

```json
{
    "apiVersion": "deployment.margo/v1",
    "kind": "DeploymentStatus",
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
                "message ": ""
            }
        }
    ]
}
```

### Response Code

| Code | Description |
|------|-------------|
| 201  | The deployment status was added, or updated, successfully |
| 4XX-5XX | The requests was not completed sucessfully |
