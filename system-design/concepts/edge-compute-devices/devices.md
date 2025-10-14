# Devices

Margo devices are defined by the roles they can facilitate within the Margo architecture. Each role has its own requirements which enable unique functionality. Edge compute within Margo is initially referenced as a "Device" which represents the initial lifecycle stage. Once the device is onboarded within the workload fleet manager, it assumes a role based on capabilities.

Supported device roles are shown below:

- Standalone Cluster
- Standalone Device

> Note: Additional device roles will be introduced over time. For example, the following roles are currently being discussed for future consideration:
>
>- Multinode Cluster Leader
>
>- Multinode Cluster Worker
>
>- Leaf Device
>
>- Gateway

## Standalone Cluster Role Details

The standalone cluster role within Margo describes devices with enough compute capacity to enable a wide range of functions within the ecosystem. Standalone clusters are single devices acting as both a cluster leader and worker node.

Currently, standalone cluster devices are expected to run Kubernetes as the orchestration platform. This role is designed to provide flexibility and scalability for Margo compliant workloads.

## Standalone Device Role Details

The standalone device role represents a device that can host Margo compliant workloads. This device role is not intended to be utilized within a clustered configuration and typically consists of devices with limited resources to run workloads.

Currently, standalone devices are expected to run Compose compliant software as the orchestration platform. This role is designed for devices where a full Kubernetes cluster is not required or feasible.
