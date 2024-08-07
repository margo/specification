# Device Capability

The purpose of the device capability reporting is to ensure the workload orchestration service has the information needed to pair workloads with compatible edge devices. The [device's capabilities](../../margo-api-reference/workload-api/device-api/device-capabilities.md) are reported to the workload orchestration web service using the via the Margo API.

## Device Capability Reporting

The device owner MUST report their device's capabilities and characteristics via the [Device API](../../margo-api-reference/workload-api/device-api/device-capabilities.md) when onboarding the device with the workload orchestration service and whenever any workload related hardware changes occur.

The following information MUST be present be provided:

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
