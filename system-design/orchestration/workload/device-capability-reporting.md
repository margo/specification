# Margo Device Capability Discovery 

The Workload Orchestration Software is informed of the Device Capabilities via the Margo Management Interface. The purpose of the capability reporting is to ensure the WOS has the information needed to pair Workloads with compatible Edge Devices. An additional benefit to the capability reporting is ensuring the WOS can accurately track resources and free space available on the Edge Device. 

## Device Capability Required Information
The Device Owner shall provide the capabilities and characteristics of their Device via the REST API interface. 

The following information MUST be present in the message:

- Device Id
- Device Vendor
- Model Number
- Serial Number
- Margo Device Role Designation(Cluster Leader/Worker / Standalone Device)
- Resources available for workloads to utilize on the Device:
	- Memory Capacity
	- Storage Capacity
	- CPU information
- Device peripherals(i.e. Graphics card)
- Network interfaces(wifi/eth/cellular)


## Device Capabilities Reporting 
This interface function ensures the the WOS is aware of the current workload device related capabilities. The Device Owner is responsible for monitoring the device and ensuring the information is accurate throughout the lifecycle of the device. 

The interface MUST provide the following functions:

1. Upon Management Interface onboarding, the interface shall send the current Device Capabilities information
2. Anytime workload related hardware changes occur, the interface MUST update the WOS.

> Note: See example device capabilities file below for structure and required information. 

**Example Device Capabilities File**

The following shall be included in the body of the API POST to inform the WOS of the device capabilities. 
```
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
			"cpu": [{
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

**Device Capability Attributes**
**Top-level Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `DeviceCapabilities`.|
| properties        | Properties    | Y    | Metadata element specifying characteristics about the device. See the [Properties](#properties-attributes) section below. |

**Properties Atrributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| id     | string    | Y    | Unique deviceID assigned to the device via the Device Owner.|
| vendor        | string    | Y    | Defines the device vendor.|
| modelNumber        | string    | Y    | Defines the model number of the device.|
| serialNumber       | string    | Y    | Defines the servial number of the device.|
| roles         | []string    | Y    | Spec element that defines the device role it can provide to the Margo environment. MUST be one of the following: Standalone Cluster, Cluster Leader, or Standalone Device |
| resources            | Device Resources    | Y    | Spec element that defines the device's resources available to the application deployed on the device. See the [Device Resources](#device-resources) section below. |
| peripherals            | Device Peripherals    | Y    | Spec element that defines the device's peripherals available to the application deployed on the device. See the [Device Peripherals](#device-peripherals) section below. |
| interfaces            | Device Interfaces    | Y    | Spec element that defines the device's interfaces that are available to the application deployed on the device. See the [Device Interfaces](#device-interfaces) section below. |


**Device Resources**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| cpuArchitecture      | string    | Y    | Defines the CPUs architecture. i.e. ARM/Intel x86.|
| cores        | integer    | Y    | Defines the cores available within the hosts CPU.|
| frequency    | integer    | Y    | Defines the frequency of the CPU. Must be defined in Ghz.|
| memory       | integer    | Y    | Defines the memory capacity available for applciations on the device. This MUST be defined in GBs|
| storage      | integer    | Y    | Defines the storage capacity available for applications to utilize. This MUST be defined in GBs.|

**Device Peripherals**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| peripheral      | []Peripheral    | Y    | Defines a peripheral that is present on the edge device. Can be one to many described in this section. See the [Peripheral Attributes](#peripheral-attributes) section below.|

**Peripheral Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the peripheral.|
| type      | string    | Y    | Type of the peripheral. i.e. GPU|
| modelNumber      | string    | Y    | Model number of the peripheral.|
| properties      | string    | Y    | Properties of the peripheral.|

**Device Interfaces**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| interface      | Interface    | Y    | Defines a interface that is present on the edge device. Can be one to many described in this section. See the [Interface Attributes](#interface-attributes) section below.|

**Interface Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the interface.|
| type      | string    | Y    | Type of the interface. i.e. Ethernet NIC, |
| modelNumber      | string    | Y    | Model number of the interface.|
| properties      | string    | Y    | Properties of the interface to inform the WOS with additional information.|

> Note: Discusssion still needed on "types" and "properties" per type that would be required. This is relevant for both the peripherals and interfaces section.