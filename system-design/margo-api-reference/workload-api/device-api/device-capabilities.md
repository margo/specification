# Device Capabilities

Devices MUST provide the Workload Fleet Management service with its capabilities and characteristics. This is done by calling the Device API's `device capabilities` endpoint.

To ensure the WFM is kept up to date, the device's client MUST send updated capabilities information if any changes occur to the information originally provided (i.e., additional memory is added to the device).

### Route and HTTP Methods

```https
POST /api/v1/device/{deviceId}/capabilities
PUT /api/v1/device/{deviceId}/capabilities
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {deviceId} | string | Y | The device's Id registered with the workload orchestration web service during onboarding.|

### Request Body Attributes

| Field      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `DeviceCapabilities`.|
| properties        | Properties    | Y    | Element that defines characteristics about the device. See the [Properties Fields](#properties-fields) section below. |

### Properties Attributes

| Field       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| id     | string    | Y    | Unique deviceID assigned to the device via the Device Owner.|
| vendor        | string    | Y    | Defines the device vendor.|
| modelNumber        | string    | Y    | Defines the model number of the device.|
| serialNumber       | string    | Y    | Defines the serial number of the device.|
| roles         | []string    | Y    | Element that defines the device role it can provide to the Margo environment. MUST be one of the following: Standalone Cluster, Cluster Leader, or Standalone Device |
| resources            | []Resource    | Y    | Element that defines the device's resources available to the application deployed on the device. See the [Resource Fields](#resources-attributes) section below. |

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

## Enumerations
These enumerations are used as vocabularies for attribute values of the `DeviceCapabilities`.

### CpuArchitectureType

| Permissible Values | Description |
| --- | --- |
| amd64 | AMD 64-bit architecture.|
| x86_64 | x86 64-bit architecture.|
| arm64 | ARM 64-bit architecture.|
| arm | ARM 32-bit architecture. |  

### CommunicationInterfaceType

| Permissible Values | Description |
| --- | --- |
| ethernet | This type stands for an Ethernet interface.|
| wifi | This type stands for an WiFi interface.|
| cellular | This type stands for cellular communication technologies such as 5G, LTE, 3G, 2G, ....|
| bluetooth | This type stands for a Bluetooth or Bluetooth Low-Energy (BLE) interface. |  
| usb | This type stands for a USB interface.|
| canbus | This type stands for a CANBus interface.|
| rs232 | This type stands for a RS232 interface. |  

### PeripheralType

| Permissible Values | Description |
| --- | --- |
| gpu | This type stands for a Graphics Processing Unit (GPU) peripheral.|
| display | This type stands for a display peripheral.|
| camera | This type stands for a camera peripheral.|
| microphone | This type stands for a microphone peripheral. |
| speaker | This type stands for a speaker peripheral. |


### Example Request

```json
{
    "apiVersion": "device.margo/v1",
    "kind": "DeviceCapabilities",
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

### Response Code

| Code | Description |
|------|-------------|
| 201  | The device capabilities document was added, or updated, successfully |
| 4XX-5XX | The requests was not completed successfully |
