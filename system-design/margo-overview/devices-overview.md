# Device Overview

Within Margo, devices are represented by compute hardware that host Margo compliant workloads within the customers environment. Devices are defined by the roles they can provide the Margo ecosystem. Each role has it's own requirements which enable unique functionality such as cluster management. These Margo device ensure the Workload Developers with garaunteed functionality they can depend on being present in every compliant device. These devices are onboarded and managed by a single Workload Fleet Manager. 

The promise the Margo specification provides Device vendors the following benefits:

- By producing a Margo compliant device it is compatible with ALL Margo compliant Fleet Managers
- Device vendors have freedom of implementation regarding the specific components, i.e. oci container runtime, as long as the component provides the agreed upon functionality the Application Vendors expect.  

Supported Device roles are shown below:

- Standalone Cluster
- Cluster Leader
- Cluster Worker
- Standalone Device
> Note: Additional device roles will be introduced as the specification matures. 

## Relevant Links
Please follow the subsuquent links to view more technical information regarding Margo compliant devices:

- [Device Requirements](../device-interoperability/device-requirements.md)
- [Collecting Application Observability Data](../device-interoperability/collecting-workload-observability-data.md)