# Device Requirements

Within Margo, devices are represented by compute hardware that runs within the customers environment to host Margo Compliant Applications. Margo Devices are defined by the roles they can facilitate within the Margo Architecture. An Edge Compute within Margo is initially referenced as a "Device" which represents the initial lifecycle stage. Once the device is onboarded within the Workload Orchestration Software, it assumes a role based on capabilities.

Supported Device roles are shown below:

- Standalone Cluster
- Cluster Leader
- Cluster Worker
- Standalone Device

> Note: Additional device roles will be introduced as the specification matures. 

## Base device requirements

- TPM support
- Secure Boot
- Attestation
- Zero Trust Network Access (ZTNA)

## Cluster Leader Role Details

The Cluster Leader Role within Margo describes devices that have the ability to manage the cluster of one or more worker nodes that are connected. Additionally, Cluster Leader can also host Margo compliant workloads.

**Cluster Leader Functional Requirements:**

- Host the Workload Fleet Management Client
    - This enables the device with the functionality outlined within the [Workload Management](../margo-overview/workload-management-interface-overview.md) section of the specification
- Enable management functionality via Kubernetes API
- Host the following additional components:
    - Helm Client (Provider)
    - OCI Container Runtime
    - OTEL Collector
    - Policy Agent
    - Host Device Fleet Management Client
        - > Note: this functionality is coming soon to the specification

## Cluster Worker Role Details

The Cluster Worker Role within Margo describes devices that have a limited amount of compute capacity that can still run Margo compliant workloads. This role is managed via the Cluster Leader.

**Cluster Worker Functional Requirements:**

- Enable Worker Node functionality within a Kubernetes Cluster via the kublet service.
- Host the following additional components:
    - OCI Container Runtime
    - OTEL Collector
    - Policy Agent
    - Host Device Fleet Management Client
        - > Note: this functionality is coming soon to the specification

## Standalone Cluster Role Details

The Standalone Cluster Role within Margo describes devices that have additional compute capacity to enable a wide range of functions within the ecosystem.

**Standalone Cluster functional requirements:**

- Enables both Cluster Leader and Worker roles concurrently in a single device
    1. See Cluster Leader Role and Cluster Worker Role for specific requirements
- The Standalone Cluster role has the ability to transition into either the Cluster Leader or Cluster Worker at a later stage in its lifecycle deployment.

## Standalone Device Role Details

The Standalone Device role represents a device that can host Margo Compliant Workloads. This device role is not intended to be utilized within a clustered configuration and typically consists of devices within limited amount of resources to run workloads.

**Standalone Device functional requirements:**

- Host the Workload Fleet Management Client
    - This enables the device with the functionality outlined within the [Workload Management](../margo-overview/workload-management-interface-overview.md) section of the specification
- Host the following additional components:
    - OCI Container Runtime
    - OTEL Collector
    - Policy Agent
    - Host Device Fleet Management Client
        - > Note: this functionality is coming soon to the specification
