# Device Capabilities

Devices MUST provide the Workload Fleet Management service with their capabilities and characteristics. This is done by calling the Device API's `device capabilities` endpoint. Reporting the device capabilities is the final step in the onboarding of the device's client. 

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
| {deviceId} | string | Y | The unique identifier of the device reporting the capabilities. <br/>It must have the following format: "{id}[/{id}[/{id}...]]". The top-level `id` is required and must include only Unreserved Characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3). The subsequent `id`s are optional, but if present they must must include only Unreserved Characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3). <br/>Using multiple ids in the endpoint does not register multiple devices in a single request, but indicates a hierarchy of devices, with a parent/child relationship. |

### Response Codes

| Code | Description |
|------|-------------|
| 201 OK | The device capabilities document was added, or updated, successfully |
| 204 No Content | The device capabilities document was deleted successfully. |
| 400 Bad Request | Missing or invalid content-digest header. Ensure the SHA256 hash of the base64-encoded payload is included. |
| 401 Unauthorized | Signature verification failed. Ensure you are signing with the correct X.509 private key.  |
| 403 Forbidden | Client certificate is not trusted or has been revoked. |
| 404 Not Found | PUT, POST:  No client with the given `clientID` was found. <br/> DELETE: No client with the given `clientID` was found or no device with the given `deviceId` was found for the client. |
| 422 Unprocessable Content | Request body includes a semantic error.  |

## Request Body Attributes

| Field      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version the API resource follows.|
| kind            | string    | Y    | Must be `DeviceCapabilitiesManifest`.|
| properties        | Properties    | Y    | Element that defines characteristics about the device. See the [Properties Fields](#properties-attributes) section below. |

### Properties Attributes

| Field       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| id     | string    | Y    | Unique deviceID assigned to the device via the Device Owner. It must include only Unreserved Characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3) plus the path separator (i.e. '/'). In case of a device behind a gateway, it takes the form of a path with the id of the parent gateway and the id of the child device, i.e., "{deviceId}/{deviceId}". The top-level {deviceId} must be unique for a given {clientId}, and the children {deviceId} must be unique for a given parent {deviceId}. |
| vendor        | string    | Y    | Defines the device vendor.|
| modelNumber        | string    | Y    | Defines the model number of the device.|
| serialNumber       | string    | Y    | Defines the serial number of the device.|
| roles         | []string    | Y    | Element that defines the device role it can provide to the Margo environment. MUST be one of the following: Standalone Cluster, Cluster Leader, Standalone Device, or Gateway |
| resources            | []Resource    | *    | Element that defines the device's resources available to the application deployed on the device. See the [Resource Fields](#resources-attributes) section below. <br/> * The element is required if the device has any of the following roles: Standalone Cluster, Cluster Leader, Standalone Device. |

### Resources Attributes
Resources of the specific device being reported to the WFM. Utilized to match with the required resources defined in the application description

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| cpu | CPU |  Y  | CPU element specifying the CPU information of the device.  See the [CPU](#cpu-attributes) section below.|
| memory | string |  Y  | The amount of memory available for applications to utilize on the device. The value is given a binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes). This is defined by the device owner.|
| storage | string |  Y  | The amount of storage available for applications to utilize on the device. The value is given a binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes, `Ti` Tebibytes, `Pi` = Pebibytes, `Ei` = Exbibytes). This is defined by the device owner.|
| peripherals | []Peripheral |  Y  | Peripherals element specifying the peripherals available for applications to utilize on the device.  See the [Peripheral](#peripheral-attributes) section below.|
| interfaces | []CommunicationInterface |  Y  | Interfaces element specifying the communication interfaces available for applications to utilize on the device.  See the [Communication Interfaces](#communicationinterface-attributes) section below.|


### CPU Attributes
CPU element defining the device's CPU characteristics.

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| cores | integer |  Y  | Defines the cores available within the hosts CPU. Specified as decimal units of CPU cores (e.g., `0.5` is half a core). This is defined by the device owner. After deployment of the application, the device MUST provide this number of CPU cores for the application.|
| architecture | CpuArchitectureType |  N  | The CPU architecture supported by the device. This can be e.g. amd64, x86_64, arm64, arm. See the [CpuArchitectureType](#cpuarchitecturetype) definition for all permissible values.|


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


## Example Device Capabilities Payload

```json
{
    "apiVersion": "device.margo.org/v1alpha1",
    "kind": "DeviceCapabilitiesManifest",
    "properties": {
        "id": "northstarida.xtapro.k8s.edge",
        "vendor": "Northstar Industrial devices",
        "modelNumber": "332ANZE1-N1",
        "serialNumber": "PF45343-AA",
        "roles": [
            "standalone cluster",
            "cluster lead"
        ],
        "resources": {
            "cpu": [
                {
                    "cores": 24,
                    "architecture": "x86_64"
                }
            ],
            "memory": "59 Gi",
            "storage": "1862 Gi",
            "peripherals": [
                {
                    "type": "GPU",
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
            ]
        }
    }
}
```

## Gateways considerations

### Opaque gateways

Opaque gateways MUST report the combined capabilities of all the devices they connect to the WFM.

> Example: An opaque gateway has two child-devices. Each child-device has an ARM64 processor with 2 cores, 5 GB of memory, 32 GB of storage, and 1 ethernet interface. The gateway will report capabilities of 4 cores, 10 GB of memory, 64 GB of storage, and 2 ethernet interfaces. In addition since the gateway can deploy compose application on its child-devices it will report the role of "standalone device".

## See-thru gateways

See-thru gateways MUST report their capabilities and the capabilities of each device they connect to the WFM. This done by calling the `device capabilities` endpoint for the gateway itself and each device. The `deviceId` in the endpoint is used to indicate the hierarchy of devices, with a parent/child relationship. For example, if a see-thru gateway with `deviceId` "gateway1" connects two devices with `deviceId` "deviceA" and "deviceB", the gateway would call the `device capabilities` endpoint three times with the following `deviceId`s: "gateway1", "gateway1/deviceA", and "gateway1/deviceB". 

When reporting its own capabilities, a see-thru gateway MUST report the role "Gateway". 

If a see-thru gateway is capable of hosting edge applications it MUST report the corresponding role(s) (i.e., "Standalone Device", "Standalone Cluster, and/or "Cluster Leader") and the resources available for these deployments.