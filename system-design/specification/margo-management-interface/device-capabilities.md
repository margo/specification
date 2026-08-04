# Device Capabilities

Devices MUST provide the Workload Fleet Management service with their capabilities and characteristics. This is done by calling the Device API's `device capabilities` endpoint. Reporting the device capabilities is the final step in the onboarding of the device's client. 

The reported capabilities represent only the subset of device resources delegated exclusively to Margo for workload placement and reconciliation, and do not necessarily reflect the device's total physical capacity. The mechanisms used to isolate, reserve, and preserve these resources for exclusive Margo use are implementation-specific and outside the scope of this specification.

To ensure the WFM is kept up to date, the device's client MUST send updated capabilities information if any changes occur to the information originally provided (i.e., additional memory is added to the device).

- Requests to this endpoint MUST be authenticated using the HTTP Message Signature method as defined in the [Payload Security](../margo-management-interface/api-requirements-and-security.md#payload-security-method) section.

## Route and HTTP Methods

```https
POST /api/v1/clients/{clientId}/capabilities/{deviceId}
PUT /api/v1/clients/{clientId}/capabilities/{deviceId}
DELETE /api/v1/clients/{clientId}/capabilities/{deviceId}
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {clientId} | string | Y | The unique identifier of the (device) client registered with the WFM during onboarding. |
| {deviceId} | string | Y | The unique identifier of the device reporting the capabilities. <br/>It must have the following format: "{id}[/{id}[/{id}...]]". The top-level `id` is required and must include only unreserved characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3). If reporting capabilties for a child device, the subsequent `id`s are required and must include only unreserved characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3). <br/>Using multiple ids in the endpoint does not register multiple devices in a single request, but indicates a hierarchy of devices, with a parent/child relationship. |

### Response Codes

| Code | Description |
|------|-------------|
| 201 OK | The device capabilities document was added, or updated, successfully |
| 204 No Content | The device capabilities document was deleted successfully. |
| 400 Bad Request | Missing or invalid content-digest header. Ensure the SHA256 hash of the base64-encoded payload is included. |
| 401 Unauthorized | Signature verification failed. Ensure you are signing with the correct X.509 private key.  |
| 403 Forbidden | Client certificate is not trusted or has been revoked. |
| 404 Not Found | POST, PUT:  No client with the given `clientID` was found, or no gateway was found for the given child-device `deviceId` (see [Gateways considerations](#gateways-considerations) for more details). <br/> DELETE: No client with the given `clientID` was found or no device with the given `deviceId` was found for the client. |
| 422 Unprocessable Content | Request body includes a semantic error.  |

## Request Body Attributes

| Field      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version the API resource follows.|
| kind            | string    | Y    | Must be `DeviceCapabilitiesManifest`.|
| properties        | Properties    | Y    | Element that defines characteristics about the device. See the [Properties Fields](#properties-attributes) section below. |
| x-&lt;unique-name&gt;-extensions | map[string]interface{} | N | Allows addition of an arbitrary JSON object whose contents suppliers use to provide vendor-specific functionality beyond what is defined in the Margo specification. See the [Specification Extensions](#specification-extensions) section below for more details. |
   

### Properties Attributes

| Field       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| id     | string    | Y    | Unique deviceID assigned to the device via the Device Owner. It must include only unreserved characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3) plus the path separator (i.e. '/'). In case of a device behind a gateway, the id field takes the form of a path with the id of the parent gateway, the id of the child device, and the ids of any intermediate devices, i.e., "{gatewayId}/[{intermediateDeviceId/.../]{deviceId}". |
| vendor        | string    | Y    | Defines the device vendor.|
| modelNumber        | string    | Y    | Defines the model number of the device.|
| serialNumber       | string    | Y    | Defines the serial number of the device.|
| cpus | []CPU | Y* | List of CPU entries available on the device. Utilized to match with the required resources defined in the application description. See the [CPU](#cpu-attributes) section below.|
| memory | string | Y* | The amount of memory available for applications to utilize on the device. The value is given in binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes). This is defined by the device owner.|
| storage | string | Y* | The amount of storage available for applications to utilize on the device. The value is given in binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes, `Ti` = Tebibytes, `Pi` = Pebibytes, `Ei` = Exbibytes). This is defined by the device owner.|
| peripherals | []Peripheral | Y* | Peripherals available for applications to utilize on the device. See the [Peripheral](#peripheral-attributes) section below.|
| interfaces | []CommunicationInterface | Y* | Communication interfaces available for applications to utilize on the device. See the [Communication Interfaces](#communicationinterface-attributes) section below.|
| otelCollector | boolean | Y* | Reports whether an OpenTelemetry (OTEL) collector is present on the device. A device that is capable of hosting workloads MUST report `true`. |
| supportedRuntimes | []SupportedRuntime | Y* | Supported workload runtimes present on the device. See the [SupportedRuntime](#supportedruntime) definition for all permissible values. A device that is capable of hosting workloads MUST report at least one entry.|
| supportedDeploymentTypes | []SupportedDeploymentType | Y* | The deployment profile types the device can receive and process locally. See the [SupportedDeploymentType](#supporteddeploymenttype) definition for all permissible values. A device that is capable of hosting workloads MUST report at least one entry.|

> Note:  \* A see-thru gateway not hosting workloads itself MUST omit these fields. The WFM infers such a device is non-hosting from the absence of these capabilities, and infers a gateway relationship from the parent/child `deviceId` hierarchy.

### CPU Attributes
CPU element defining the device's CPU characteristics.

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| cores | number |  Y  | Defines the cores available within the hosts CPU. Specified as decimal units of CPU cores (e.g., `0.5` is half a core). This is defined by the device owner. After deployment of the application, the device MUST provide this number of CPU cores for the application.|
| architecture | CpuArchitectureType |  N  | The CPU architecture supported by the device. This can be e.g. amd64, arm64, arm. See the [CpuArchitectureType](#cpuarchitecturetype) definition for all permissible values.|

Each entry in the `cpus` array describes one set of cores a single workload can be placed on. A device satisfies an application's `requiredResources.cpu` only if a single entry provides at least the required number of `cores` and, when the application specifies one or more architectures, that entry's `architecture` is one of the listed values. Cores from separate `cpus` entries MUST NOT be summed together when evaluating the requirement.


### Peripheral Attributes
Peripheral hardware of a device.

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| type | PeripheralType |  Y  | The type of peripheral. This can be e.g. GPU, display, camera, microphone, speaker. See the [PeripheralType](#peripheraltype) definition for all permissible values.|
| manufacturer | string |  N  | The name of the manufacturer.|
| model | string |  N  | The model of the peripheral.|


### CommunicationInterface Attributes
Communication interface of a device.

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| type | CommunicationInterfaceType |  Y  | The type of a communication interface. This can be e.g. Ethernet, WiFi, Cellular, Bluetooth, USB, CANBus, RS232. See the [CommunicationInterfaceType](#communicationinterfacetype) definition for all permissible values.|

### Enumerations
These enumerations are used as vocabularies for attribute values of the `DeviceCapabilities`.

#### CpuArchitectureType

| Permissible Values | Description |
| --- | --- |
| amd64 | AMD 64-bit architecture.|
| arm64 | ARM 64-bit architecture.|
| arm | ARM 32-bit architecture. |  

#### CommunicationInterfaceType

| Permissible Values | Description |
| --- | --- |
| ethernet | This type stands for an Ethernet interface.|
| wifi | This type stands for an WiFi interface.|
| cellular | This type stands for cellular communication technologies such as 5G, LTE, 3G, 2G, ....|
| bluetooth | This type stands for a Bluetooth or Bluetooth Low-Energy (BLE) interface. |  
| usb | This type stands for a USB interface.|
| canbus | This type stands for a CANBus interface.|
| rs232 | This type stands for a RS232 interface. |  

#### PeripheralType

| Permissible Values | Description |
| --- | --- |
| gpu | This type stands for a Graphics Processing Unit (GPU) peripheral.|
| display | This type stands for a display peripheral.|
| camera | This type stands for a camera peripheral.|
| microphone | This type stands for a microphone peripheral. |
| speaker | This type stands for a speaker peripheral. |

#### SupportedRuntime

| Permissible Values | Description |
| --- | --- |
| oci | OCI container runtime. |


#### SupportedDeploymentType

| Permissible Values | Description |
| --- | --- |
| helm | Device can receive and process Kubernetes Helm chart deployments locally. |
| compose | Device can receive and process Compose service deployments locally. |


## Example Device Capabilities Payload

```json
{
    "apiVersion": "device.margo.org/v1alpha1",
    "kind": "DeviceCapabilitiesManifest",
    "properties": {
        "id": "northstarida.xtapro.k8s.edge",
        "vendor": "Northstar Industrial Devices",
        "modelNumber": "332ANZE1-N1",
        "serialNumber": "PF45343-AA",
        "cpus": [
            {
                "cores": 24,
                "architecture": "amd64"
            }
        ],
        "memory": "59 Gi",
        "storage": "1862 Gi",
        "peripherals": [
            {
                "type": "gpu",
                "manufacturer": "NVIDIA"
            }
        ],
        "interfaces": [
            {
                "type": "ethernet"
            },
            {
                "type": "wifi"
            }
        ],
        "otelCollector": true,
        "supportedRuntimes": [
            "oci"
        ],
        "supportedDeploymentTypes": [
            "helm",
            "compose"
        ]
    }
}
```

## Gateways considerations

> Note: See [Gateways](../../concepts/gateways/gateways.md) page in the concepts section for more information about gateways.

### Opaque gateways

A device may represent, and aggregate the capabilities of, multiple child-devices behind it and report itself as a single Margo device to the WFM. This type of device is referred to as an opaque gateway. Opaque gateways report the combined capabilities of all the devices they connect to the WFM as a single `DeviceCapabilitiesManifest`. Because the child-devices are not individually visible to the WFM, an opaque gateway is seen as a single device and reports the aggregated resource fields, `supportedRuntimes`, and `supportedDeploymentTypes` of the devices behind it.

> Example: An opaque gateway has two child-devices. Each child-device has an ARM64 processor with 2 cores, 5 GB of memory, 32 GB of storage, and 1 ethernet interface. The gateway will report capabilities of 2 CPUs (arm64) with 2 cores each, 10 GB of memory, 64 GB of storage, and 2 ethernet interfaces. Since the gateway can deploy compose applications on its child-devices it will report `supportedDeploymentTypes: ["compose"]`.

### See-thru gateways

WFM clients may connect one or more child-devices to the WFM while allowing the WFM to see each device behind it as an individual device with its own capabilities. This type of client is referred to as a **see-thru gateway**.

A see-thru gateway uses the same `DeviceCapabilitiesManifest` schema as any other device — from a payload perspective it is an ordinary device that also reports the devices behind it. Its conformance rules are relaxed, though: unlike non-gateway device, a see-thru gateway is not required to host workloads and need not report workload-hosting capabilities. The WFM infers the gateway relationship from the parent/child `deviceId` hierarchy, which is typically most evident when the gateway reports no workload-hosting capabilities.

**How a see-thru gateway reports capabilities**

A see-thru gateway MUST report its own capabilities and the capabilities of each device it connects to the WFM:

1. Call the `device capabilities` endpoint once for the gateway itself, then once for each device behind it.
2. Encode the hierarchy in the `deviceId` as a parent/child path. For example, a gateway `gateway1` with two child-devices calls the endpoint three times, with `deviceId`s `gateway1`, `gateway1/deviceA`, and `gateway1/deviceB`.
3. Report the gateway's own manifest **before** any child manifest. If the WFM receives a child manifest first, it MUST reject the request with a `404 Not Found` response code.

**What the gateway reports about itself**

| If the gateway... | Then its own manifest MUST... |
| --- | --- |
| does **not** host workloads | contain only the required identity fields — omit the workload-hosting fields (`cpus`, `memory`, `storage`, `peripherals`, `interfaces`, `supportedRuntimes`, `supportedDeploymentTypes`), and omit `otelCollector` |
| **also** hosts workloads | report the workload-hosting fields like any hosting device, including at least one entry in both `supportedRuntimes` and `supportedDeploymentTypes` |

Hosting is neither required of nor forbidden for a see-thru gateway: it reports the workload-hosting fields when it hosts workloads, and omits them when it does not.

#### Examples

* See-thru gateway, without hosting capabilities, reporting its capabilities to the WFM:

    ```
    POST /api/v1/clients/{clientId}/capabilities/gateway1
    ```
    ```json
    {
        "apiVersion": "device.margo.org/v1alpha1",
        "kind": "DeviceCapabilitiesManifest",
        "properties": {
            "id": "gateway1",
            "vendor": "Gateway Vendor",
            "modelNumber": "GW-1000",
            "serialNumber": "GW12345678"
        }
    }
    ```

* See-thru gateway, with hosting capabilities, reporting its capabilities to the WFM:

    ```
    POST /api/v1/clients/{clientId}/capabilities/gateway1
    ```
    ```json
    {
        "apiVersion": "device.margo.org/v1alpha1",
        "kind": "DeviceCapabilitiesManifest",
        "properties": {
            "id": "gateway1",
            "vendor": "Gateway Vendor",
            "modelNumber": "GW-1000",
            "serialNumber": "GW12345678",
            "cpus": [
                {
                    "cores": 4,
                    "architecture": "amd64"
                }
            ],
            "memory": "12 Gi",
            "storage": "200 Gi",
            "peripherals": [],
            "interfaces": [
                {
                    "type": "ethernet"
                }
            ],
            "otelCollector": true,
            "supportedRuntimes": [
                "oci"
            ],
            "supportedDeploymentTypes": [
                "compose"
            ]
        }
    }
    ```

* See-thru gateway reporting the capabilities of a child device to the WFM:

    ```
    POST /api/v1/clients/{clientId}/capabilities/gateway1/deviceA
    ```
    ```json
    {
        "apiVersion": "device.margo.org/v1alpha1",
        "kind": "DeviceCapabilitiesManifest",
        "properties": {
            "id": "gateway1/deviceA",
            "vendor": "Device A Vendor",
            "modelNumber": "DA-2000",
            "serialNumber": "DA12345678",
            "cpus": [
                {
                    "cores": 24,
                    "architecture": "amd64"
                }
            ],
            "memory": "59 Gi",
            "storage": "1862 Gi",
            "peripherals": [
                {
                    "type": "gpu",
                    "manufacturer": "NVIDIA"
                }
            ],
            "interfaces": [
                {
                    "type": "ethernet"
                }
            ],
            "otelCollector": true,
            "supportedRuntimes": [
                "oci"
            ],
            "supportedDeploymentTypes": [
                "helm"
            ]
        }
    }
    ```

* See-thru gateway reporting the capabilities of a child device with deeper hierarchy to the WFM:

    ```
    POST /api/v1/clients/{clientId}/capabilities/gateway1/path1/deviceA
    ```
    ```json
    {
        "apiVersion": "device.margo.org/v1alpha1",
        "kind": "DeviceCapabilitiesManifest",
        "properties": {
            "id": "gateway1/path1/deviceA",
            "vendor": "Device A Vendor",
            "modelNumber": "DA-1000",
            "serialNumber": "DA12345678",
            "cpus": [
                {
                    "cores": 2,
                    "architecture": "arm64"
                }
            ],
            "memory": "6 Gi",
            "storage": "30 Gi",
            "peripherals": [],
            "interfaces": [
                {
                    "type": "ethernet"
                }
            ],
            "otelCollector": true,
            "supportedRuntimes": [
                "oci"
            ],
            "supportedDeploymentTypes": [
                "compose"
            ]
        }
    }
    ```

* See-thru gateway informing the WFM that a child device is no longer available:

    ```
    DELETE /api/v1/clients/{clientId}/capabilities/gateway1/deviceA
    ```

## Specification Extensions

> **Note:** See the [specification extensions](../margo-management-interface/specification-extensions.md) page for additional details.

The Device Capabilities document supports the following specification extension scenarios:

### Collaboration between device and workload fleet manager suppliers

For the device workload fleet manager clients to make use of specification extensions defined by a workload fleet manager supplier, the extension property MUST be added to the device capabilities JSON document's [root](#request-body-attributes).

Workload fleet manager service implementations MUST ignore any unknown specification extensions targeting a device supplier. Importing a device capabilities document with unknown specification extensions MUST NOT result in a failure because of the included specification extensions.