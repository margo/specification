# Edge Compute Devices

Within Margo, devices are represented by compute hardware that host Margo compliant workloads within the customer's environment. Margo compliant device ensure the workload developers with guaranteed functionality they can depend on being present in every device.

The Margo specification provides device vendors the following benefits:

- By producing a Margo compliant device it is compatible with ALL Margo compliant fleet managers
- Device vendors have freedom of choice regarding the specific components (i.e. OCI container runtime) they choose as long as the component provides the agreed upon functionality the application vendors expect.

## Margo Device layers

Margo devices consist of three major layers: Margo interface layer, platform layer, traditional device layer. Although Margo requires compliance towards its requirements, such as hosting the Margo management interface client, the device vendor has freedom to implement as they see fit. 

Below is a diagram that depicts the device layers along with some examples: 

![Device Layer Drawing)](../figures/device-layers.drawio.svg)

## Relevant Links

Please follow the subsequent links to view more technical information regarding Margo compliant devices:

- [Device Concepts](../device-interoperability/devices.md)
- [Collecting Application Observability Data](../device-interoperability/collecting-workload-observability-data.md)