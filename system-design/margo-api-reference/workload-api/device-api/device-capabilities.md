# Device Capabilities

Devices MUST provide the workload orchestration service with its capabilities and characteristics. This is done by calling the Device API's `device capabilities` endpoint.

### Route and HTTP Methods

```http
POST /device/{deviceId}/capabilities
PUT /device/{deviceId}/capabilities
```

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {deviceId} | string | Y | The device's Id registered with the workload orchestration web service during onboarding.|

### Request Body Fields

> Action: Discusssion still needed on "types" and "properties" per type that would be required. This is relevant for both the peripherals and interfaces section.

| Field      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `DeviceCapabilities`.|
| properties        | Properties    | Y    | Element that defines characteristics about the device. See the [Properties Fields](#properties-fields) section below. |

#### Properties Fields

| Field       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| id     | string    | Y    | Unique deviceID assigned to the device via the Device Owner.|
| vendor        | string    | Y    | Defines the device vendor.|
| modelNumber        | string    | Y    | Defines the model number of the device.|
| serialNumber       | string    | Y    | Defines the serial number of the device.|
| roles         | []string    | Y    | Element that defines the device role it can provide to the Margo environment. MUST be one of the following: Standalone Cluster, Cluster Leader, or Standalone Device |
| resources            | []Resource    | Y    | Element that defines the device's resources available to the application deployed on the device. See the [Resource Fields](#resources-fields) section below. |
| peripherals            | []Peripheral    | Y    | Element that defines the device's peripherals available to the application deployed on the device. See the [Peripheral Fields](#peripheral-fields) section below. |
| interfaces            | []Interface    | Y    | Element that defines the device's interfaces that are available to the application deployed on the device. See the [Interface Fields](#interface-fields) section below. |

#### Resources Fields

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| cpus         | []CPU      | Y    | Element that defines the device's CPUs that are available to the application deployed on the device. See the [CPU Fields](#cpu-fields) section below.|
| memory       | integer    | Y    | Defines the memory capacity available for applciations on the device. This MUST be defined in GBs|
| storage      | integer    | Y    | Defines the storage capacity available for applications to utilize. This MUST be defined in GBs.|

#### CPU Fields

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| cpuArchitecture      | string    | Y    | Defines the CPUs architecture. i.e. ARM/Intel x86.|
| cores        | integer    | Y    | Defines the cores available within the hosts CPU.|
| frequency    | integer    | Y    | Defines the frequency of the CPU. Must be defined in Ghz.|

#### Peripheral Fields

| Fields      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the peripheral.|
| type      | string    | Y    | Type of the peripheral. i.e. GPU|
| modelNumber      | string    | Y    | Model number of the peripheral.|
| properties      | map[string]string    | Y    | Properties of the peripheral.|

#### Interface Fields

| Fields      | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the interface.|
| type      | string    | Y    | Type of the interface. i.e. Ethernet NIC, |
| modelNumber      | string    | Y    | Model number of the interface.|
| properties      | map[string]string   | Y    | Properties of the interface to inform the WOS with additional information.|

### Example Request

```json
{
    "apiVersion": "device.margo/v1",
    "kind": "DeviceCapability",
    "properties": {
        "id": "northstarida.xtapro.k8s.edge",
        "vendor": "Northstar Industrial Applications",
        "modelNumber": "332ANZE1-N1",
        "serialNumber": "PF45343-AA",
        "roles": ["standalone cluster", "cluster lead"],
        "resources": {
            "memory": "64.0 GB",
            "storage": "2000 GB",
            "cpus": [{
                "architecture": "Intel x64",
                "cores": 24,
                "frequency": "6.2 GHz"
            }]
        },
        "peripherals": [{
            "name": "NVIDIA GeForce RTX 4070 Ti SUPER OC Edition Graphics Card",
            "type": "GPU",  
            "modelNumber": "TUF-RTX4070TIS-O16G",
            "properties": {
                "manufacturer": "NVIDIA",
                "series": "NVIDIA GeForce RTX 40 Series",
                "gpu": "GeForce RTX 4070 Ti SUPER",
                "ram": "16 GB",
                "clockSpeed": "2640 MHz"
            }
        }],
        "interfaces": [
            {
                "name": "RTL8125 NIC 2.5G Gigabit LAN Network Card",
                "type": "Ethernet",
                "modelNumber": "RTL8125",
                "properties": {
                    "maxSpeed": "2.5 Gbps"
                }
            },
            {
                "name": "WiFi 6E Intel AX411NGW M.2 Cnvio2",
                "type":  "Wi-Fi",
                "modelNumber": "AX411NGW",
                "properties": {
                    "bands": ["2.4 GHz", "5 GHz", "6GHz"],
                    "maxSpeed": "2.4 Gbps"
                }
            }]
    }
}
```

### Response Code

| Code | Description |
|------|-------------|
| 201  | The device capabilities document was added, or updated, successfully |
| 4XX-5XX | The requests was not completed sucessfully |
