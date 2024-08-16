# Device Capability

The purpose of device capabilities reporting is to ensure the workload orchestration solution has the information needed to pair workloads with compatible edge devices. The [device's capabilities](../../margo-api-reference/workload-api/device-api/device-capabilities.md) are reported to the workload orchestration web service using [Margo management API](../../margo-api-reference/margo-api-specification.md).

### Device Capability Reporting

The device owner MUST report their device's capabilities and characteristics via the [Device API](../../margo-api-reference/workload-api/device-api/device-capabilities.md) when onboarding the device with the workload orchestration solution and whenever any workload related hardware changes occur.

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
