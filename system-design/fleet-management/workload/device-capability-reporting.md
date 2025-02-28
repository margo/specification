# Device Capabilities

The purpose of device capabilities reporting is to ensure the Workload Fleet Management solution has the information needed to pair workloads with compatible edge devices. The [device's capabilities](../../margo-api-reference/workload-api/device-api/device-capabilities.md) are reported to the workload orchestration web service using [Margo management API](../../margo-api-reference/margo-api-specification.md).

### Device Capability Reporting

The device owner MUST report their device's capabilities and characteristics via the [Device API](../../margo-api-reference/workload-api/device-api/device-capabilities.md) when onboarding the device with the workload orchestration solution. Additionally, during the lifecycle of the Edge device, if there is a change that impacts the reported characteristics, the device's interface shall send an update to the Workload Fleet Manager. 

> Action: The device capabilities details are still being discussed

The following information MUST be provided:

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

For more information see the [device capabilties API](../../margo-api-reference/workload-api/device-api/device-capabilities.md).
