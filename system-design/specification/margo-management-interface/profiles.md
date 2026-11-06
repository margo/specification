# Profiles

Workload targets MUST provide the workload fleet management service with their characteristics in order for workloads to be matched with appropriate workload targets. This is done by calling the `profile` endpoint. Reporting the workload target's profile is the first exchange a workload fleet manager client makes after provisioning and connecting to the workload fleet manager service.

The reported profile represent the characteristics delegated exclusively to Margo for workload placement and reconciliation, and may not reflect a workload target's total physical capacity or characteristics. The mechanisms used to isolate, reserve, and preserve these resources for exclusive Margo use are implementation-specific and outside the scope of this specification.

To ensure the workload fleet manager has the latest profile information, the workload fleet manager client MUST send updated profile information if any changes occur to the information originally provided (i.e., additional memory is added, GPU becomes allocated, etc.).

In order to decouple the core specification from the individual deployment technology specifications, the workload fleet manager services it not expected to understand the reported profile characteristic schemas. Workload fleet manager services are only required to use the profile information to evaluate matching criteria defined in the `ApplicationDescription`. This decoupling allows deployment technology specifications to be update or added without requiring workload fleet manager implementations to change.

> **Note:** Margo cannot prevent workload fleet manager suppliers from tightly coupling their implementation to these schemas, but suppliers assume the risk introduced by tight coupling.

## Route and HTTP Methods

```https
PUT /api/v1/profile/{workloadTargetId}
DELETE /api/v1/profile/{workloadTargetId}
```

- PUT creates or replaces. Profile updates MUST be atomic.
- DELETE removes the complete profile for the workload target.

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {workloadTargetId} | string | Y | The unique identifier of the workload target reporting the profile.|

Requests MUST use the following format: `{workloadTargetId}[/{workloadTargetId}]`

- The top-level `workloadTargetId` is required.
- The subsequent `workloadTargetId` is required when reporting profiles for a child workload targets.
- `workloadTargetId` MUST include only unreserved characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3).

Using multiple `workloadTargetId` in the endpoint does not register multiple workload target in a single request. The parent workload target's profile MUST be registered prior to registering child workload targets.

The workload fleet manger client reporting the profile(s) is responsible for assigning and maintaining the workload target IDs used for each reported workload target profile.

Workload fleet managers MUST use the exact `workloadTargetId` or `workloadTargetId/workloadTargetId` route used to report the profile as the `metadata.deviceId` in the [ApplicationDeployment manifest](desired-state.md#applicationdeployment-yaml-definition).

### Response Codes

| Code | Description |
|------|-------------|
| 200 OK | The profile document was updated successfully. |
| 201 Created | The profile document was created successfully. |
| 204 No Content | The profile document was deleted successfully. |
| 400 Bad Request | PUT: Malformed request body. |
| 403 Forbidden | The request is not authorized by the workload fleet manager's local policy (for example, the client relationship has been retired; see [Authorization](../identity/wfm-identity-profile.md#authorization)). |
| 404 Not Found | PUT: No gateway was found for the client for the given child `workloadTargetId` (see [Gateways considerations](#gateways-considerations) for more details). <br/> DELETE: No workload target with the given `workloadTargetId` was found for the client. |
| 422 Unprocessable Content | Request body includes a semantic error.  |

## Request Body Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| characteristics | characteristic[] | Y | List of characteristic entries composing the workload target's profile.|
| x-&lt;unique-name&gt;-extensions | map[string]interface{} | N | Allows addition of an arbitrary JSON object whose contents suppliers use to provide vendor-specific functionality beyond what is defined in the Margo specification. See the [Specification Extensions](#specification-extensions) section below for more details. |

> **Note:** The individual deployment technology specifications will define which characteristics should be reported. For now, report whatever characteristics are applicable from the temporary [Common Characteristics](#common-characteristics) described below.

## Characteristic Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| key | string | Y | A unique key assigned to the characteristic and used in the `ApplicationDescription` to identify which characteristic the match expression is targeting. |
| properties | interface{} | Y | A JSON property bag containing the characteristic's properties. Workload fleet manager implementations are not expected to understand characteristics schemas. |

## Example Profile Payload

```json
{
    "characteristics": [{
        "key": "margo.org/nameplate",
        "properties": {
            "vendor": "Northstar Industrial Devices",
            "modelNumber": "332ANZE1-N1",
            "serialNumber": "PF45343-AA"
        }
    },{
        "key": "margo.org/resource/cpu",
        "properties": {
            "cpus": [{
                "cores": 24,
                "architecture": "amd64"
            }]
        }
    },{
        "key": "margo.org/resource/memory",
        "properties": {
            "available": 59
        }
    },{
        "key": "margo.org/resource/storage",
        "properties": {
            "available": 1862
        }
    },{
        "key": "margo.org/peripherals",
        "properties": {
            "peripherals": [{
                "type": "gpu",
                "manufacturer": "NVIDIA"
            }]
        }
    },{
        "key": "margo.org/interfaces",
        "properties": {
            "interfaces": [{
                "type": "ethernet"
            },{
                "type": "wifi"
            }]
        }
    },{
        "key": "margo.org/services",
        "properties": {
            "otelCollector": true
        }
    },{
        "key": "margo.org/deployment/compose",
        "properties": {}
    },{
        "key": "margo.org/deployment/helm",
        "properties": {}
    }]
}
```

## Gateways considerations

> Note: See [Gateways](../../concepts/gateways/gateways.md) page in the concepts section for more information about gateways.

### Opaque gateways

A workload fleet manager client may represent multiple child-workload targets by reporting a single aggregate profile to the workload fleet manager. This type of profile is referred to as an opaque gateway. Opaque gateways report the combined characteristics of all the workload targets to the WFM as a single `profile`. Because the child-workload targets are not individually visible to the WFM, an opaque gateway is seen as a single workload target and reports the aggregated characteristics for all child-workload targets the gateway represents.

> Example: An opaque gateway has two child-workload targets. Each child-workload target has an ARM64 processor with 2 cores, 5 GB of memory, 32 GB of storage, and 1 ethernet interface. The gateway will report a profile for 2 CPUs (arm64) with 2 cores each, 10 GB of memory, 64 GB of storage, and 2 ethernet interfaces. Since the gateway supports the compose deploy technology on its child-workload target it will report support for the `margo.org/deployment/compose` characteristic.

### See-thru gateways

A workload fleet manager client may connect one or more child-workload targets to the workload fleet manager while allowing the workload fleet manager to see each workload target behind individually with its own `profile`. This type of representation is referred to as a **see-thru gateway**.

A see-thru gateway uses the same `profile` schema as any other workload target — from a payload perspective it is an ordinary workload target that also reports the workload targets behind it. Its conformance rules are relaxed, though: a see-thru gateway is not required to host workloads. The workload fleet manager infers the gateway relationship from the parent/child `workloadTargetId` hierarchy, which is typically most evident when the gateway reports no workload-hosting characteristics.

#### How a see-thru gateway reports profiles

A see-thru gateway MUST report its own profile and the profiles of each workload targets it connects to the workload fleet manager:

1. Call the `profile` endpoint once for the gateway itself, then once for each workload target behind it.
2. Encode the hierarchy in the `workloadTargetId` as a parent/child path in the route. For example, a gateway `gateway1` with two child-workload targets calls the endpoint three times, with `workloadTargetId`s of `profile/gateway1`, `profile/gateway1/targetA`, and `profile/gateway1/targetB`.
3. Report the gateway's own profile **before** any child profiles. If the workload fleet manager receives a child profile first, it MUST reject the request with a `404 Not Found` response code.

#### What the gateway reports about itself

- If the Gateway hosts workloads, it should report all applicable characteristics to enable `ApplicationDefinition` match expressions to be matched with the workload target.
- If the Gateway does not host workloads, it reports a profile with an empty characteristics array since workloads will not need be matched with the Gateway.

#### Examples

- A See-thru gateway incapable of hosting workloads reporting its profile to the workload fleet manager:

    ```http
    PUT /api/v1/profile/gateway1
    ```

    ```json
    {
        "characteristics": []
    }
    ```

- A See-thru gateway capable of hosting workloads reporting its profile to the workload fleet manager:

    ```http
    PUT /api/v1/profile/gateway1
    ```

    ```json
    {
        "characteristics": [{
            "key": "margo.org/nameplate",
            "properties": {
                "vendor": "Gateway Vendor",
                "modelNumber": "GW-1000",
                "serialNumber": "GW12345678"
            }
        },{
            "key": "margo.org/resource/cpu",
            "properties": {
                "cpus": [{
                    "cores": 4,
                    "architecture": "amd64"
                }]
            }
        },{
            "key": "margo.org/resource/memory",
            "properties": {
                "available": 12
            }
        },{
            "key": "margo.org/resource/storage",
            "properties": {
                "available": 200
            }
        },{
            "key": "margo.org/interfaces",
            "properties": {
                "interfaces": [{
                    "type": "ethernet"
                }]
            }
        },{
            "key": "margo.org/services",
            "properties": {
                "otelCollector": true
            }
        },{
            "key": "margo.org/deployment/compose",
            "properties": {}
        }]
    }
    ```

- A See-thru gateway reporting a child workload target's profile to the workload fleet manager:

    ```http
    PUT /api/v1/profile/gateway1/deviceA
    ```

    ```json
    {
        "characteristics": [{
            "key": "margo.org/nameplate",
            "properties": {
                "vendor": "Vendor ABC",
                "modelNumber": "DA-2000",
                "serialNumber": "DA12345678"
            }
        },{
            "key": "margo.org/resource/cpu",
            "properties": {
                "cpus": [{
                    "cores": 24,
                    "architecture": "amd64"
                }]
            }
        },{
            "key": "margo.org/resource/memory",
            "properties": {
                "available": 59
            }
        },{
            "key": "margo.org/resource/storage",
            "properties": {
                "available": 1862
            }
        },{
            "key": "margo.org/peripherals",
            "properties": {
                "peripherals": [{
                    "type": "gpu",
                    "manufacturer": "NVIDIA"
                }]
            }
        },{
            "key": "margo.org/interfaces",
            "properties": {
                "interfaces": [{
                    "type": "ethernet"
                }]
            }
        },{
            "key": "margo.org/services",
            "properties": {
                "otelCollector": true
            }
        },{
            "key": "margo.org/deployment/helm",
            "properties": {}
        }]
    }
    ```

- See-thru gateway informing the workload fleet manager to remove a child workload target's profile:

    ```http
    DELETE /api/v1/profile/gateway1/deviceA
    ```

## Common Characteristics

> **Note:** The following are temporary characteristics based on what was defined previously for device capabilities to maintain compatibility until new characteristics can be defined as part of separating the core specification from the individual deployment technology specifications.

### Nameplate

Key: `margo.org/nameplate`

#### Nameplate Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| vendor | string | Y | Defines the workload target's vendor. |
| modelNumber | string | Y | Defines the workload target's model number. |
| serialNumber | string | Y | Defines the workload target's serial number. |

#### Nameplate Example

```json
{
    "key": "margo.org/nameplate",
    "properties": {
        "vendor": "NorthGate Assemblies",
        "modelNumber": "DA-2022123B",
        "serialNumber": "DA20A2349A-1",
    }
}
```

### CPUs

Key: `margo.org/resource/cpu`

#### CPUs Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| cores | number | Y | Defines how many cores the CPU has available. Specified as decimal units of CPU cores (e.g., 0.5 is half a core). This is defined by the workload target owner. |
| architecture | enum | N | Define the CPU's architecture. Must be `amd64`, `arm64` or `arm` |

#### CPUs Example

```json
{
    "key": "margo.org/resource/cpu",
    "properties": {
        "cpus": [{
            "cores": 12,
            "architecture": "amd64"
        },{
            "cores": 12,
            "architecture": "amd64"   
        }]
    }
}
```

### Memory

Key: `margo.org/resource/memory`

#### Memory Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| available | number | Y | The amount of memory, in Gibibytes, available for workloads to utilize on the workload target. |

#### Memory Example

```json
{
    "key": "margo.org/resource/memory",
    "properties": {
        "available": 64
    }
}
```

### Storage

Key: `margo.org/resource/storage`

#### Storage Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| available | number | Y | The amount of storage, in Gibibytes, available for workloads to utilize on the workload target. |

#### Storage Example

```json
{
    "key": "margo.org/resource/storage",
    "properties": {
        "available": 1862
    }
}
```

### Peripherals

Indicates the peripherals available on the workload target.

Key: `margo.org/peripherals`

#### Peripherals Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| type | enum | Y | The type of peripheral available on the workload target. Must be `gpu`, `display`, `camera`, `microphone` or `speaker` |
| manufacturer | string | N | The name of the manufacturer. |
| model | string | N | The model of the peripheral. |

#### Peripherals Example

```json
{
    "key": "margo.org/peripherals",
    "properties": {
        "peripherals": [{
            "type": "gpu",
            "manufacturer": "NVIDIA",
        },{
            "type": "microphone"
        }]
    }
}
```

### Interfaces

Indicates the interfaces available on the workload target.

Key: `margo.org/interfaces`

#### Interfaces Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| type | enum | Y | The type of interfaces available on the workload target. Must be `ethernet`, `wifi`, `cellular`, `bluetooth`, `usb`, `canbus`, or `rs232` |

#### Interfaces Example

```json
{
    "key": "margo.org/interfaces",
    "properties": {
        "interfaces": [{
            "type": "ethernet",
        },{
            "type": "wifi"
        }]
    }
}
```

### Services

Indicates the services available on the workload target.

Key: `margo.org/services`

#### Services Properties Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| otelCollector | boolean | Y | Reports whether an OpenTelemetry (OTEL) collector is present on the workload target. A workload target capable of hosting workloads MUST report `true`. |

#### Services Example

```json
{
    "key": "margo.org/services",
    "properties": {
        "otelCollector": true
    }
}
```

### Compose Deployment Technology Support

Indicates the workload target is capable of deploying Compose workloads.

Key: `margo.org/deployment/compose`

#### Compose Deployment Technology Properties Attributes

> **Note:** The properties for the compose deployment technology will be defined once the deployment technology specifications are separated from the core specification.

#### Compose Deployment Technology Example

```json
{
    "key": "margo.org/deployment/compose",
    "properties": {}
}
```

### Helm Deployment Technology Support

Indicates the workload target is capable of deploying Helm workloads.

Key: `margo.org/deployment/helm`

#### Helm Deployment Technology Properties Attributes

> **Note:** The properties for the helm deployment technology will be defined once the deployment technology specifications are separated from the core specification.

#### Helm Deployment Technology Example

```json
{
    "key": "margo.org/deployment/helm",
    "properties": {}
}
```

## Custom Deployment Technologies

> **Note:** See the [Custom Deployment Technologies](../extensibility/custom-deployment-technologies.md) page for additional details.

A workload target MAY support custom deployment technologies by defining a vendor-specific deployment technology specification which details the deployment characteristics required to support the deployment technology that has not been defined by the Margo community.

> **Note:** Need to reference the guidelines for deployment technology spec writers onces it is available.

## Specification Extensions

> **Note:** See the [specification extensions](../extensibility/specification-extensions.md) page for additional details.

The `profile` payload supports the following specification extension scenarios:

### Collaboration between device and workload fleet manager suppliers

For the device workload fleet manager clients to make use of specification extensions defined by a workload fleet manager supplier, the extension property MUST be added to the profiles JSON document's [root](#request-body-attributes).

Workload fleet manager service implementations MUST ignore any unknown specification extensions. Importing a profile with unknown specification extensions MUST NOT result in a failure because of the included specification extensions.
