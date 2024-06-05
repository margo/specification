# Margo Edge Compute Device Details

Within Margo, devices are represented by compute hardware that runs within the customers environment to host Margo Compliant Applications. Margo Devices are defined by the roles they can facilitate within the Margo Architecture. An Edge Compute within Margo is initially referenced as a "Device" which represents the initial lifecycle stage. Once the device is onboarded within the Workload Orchestration Software, it assumes a role based on capabilities. 
Supported Device roles are shown below:

- Standalone Cluster
- Cluster Leader
- Cluster Worker
- Standalone Device
- Micro Device 

**NOTE:** In Margo Version 1 only single vendor Kubernetes clusters are supported.  As such, the Cluster Worker requirements are to be managed by the vendor for Version 1.  In future versions, when multi-vendor clusters are included, the requirements of the Cluster Worker role will have to consider compatibility between the Cluster Leadar and the Cluster Worker.  This compatibility could be affected by the choosen Kubernetes distrobution, version, etc.

## Base Requirements for All Devices
- TPM support
- Secure Boot
- Attestation
- Zero Trust Network Access (ZTNA)

## Cluster Leader Role Details
The Cluster Leader Role within Margo describes devices that have the ability to manage the cluster of one or more worker nodes that are subscribed to this leader (itself included if applicable).  

**Cluster Leader Functional Requirements:**

- MUST enable control node functionality for in Kubernetes cluster 
- MUST Support minimum set of Kubernetes control node API
- MUST support Helm V3 chart(s) for application deployment.
- MUST support the "Workload Orchestration Agent" Interface 
- MUST support the telemetry API (OTEL)
- MUST support the "Policy Agent" API
- MUST support the "Device Orchestration Agent" API - out of scope for MVS1 


## Cluster Worker Role Details
The Cluster Worker Role within Margo describes devices that have a limited amount of compute capacity that can still run Margo Compliant Applications. This Role is orchestrated via the Cluster Leader.

**Cluster Worker Functional Requirements:**

- Enable Worker Node functionality within a Kubernetes Cluster
- Host the following additional components:
    - OCI Container Runtime
    - OTEL Collector
        - MUST - Leader, Stand-Alone-Cluster, or Stand-Alone-Device Nodes
        - SHOULD - Worker Node       
    - Policy Agent
    - Host Device Orchestration Agent 
        - **Note:** Out of scope for MVS1


## Standalone Cluster Role Details
The Standalone Cluster Role within Margo describes devices that have additional compute capacity to enable a wide range of functions within the ecosystem. 

**Standalone Cluster functional requirements:**

- Enables both Cluster Leader and Worker roles concurrently in a single device
    1. See Cluster Leader Role and Cluster Worker Role for specifict requirements
- The Standalone Cluster role has the ability to transition into either the Cluster Leader or Cluster Worker at a later stage in deployment. 


## Standalone Device Role Details
The Standalone Device role represents a device that can host Margo Compliant Applications. This device role is not intended to be utilized within a Kubernetes edge environment. 

**Standalone Device functional requirements:**

- Host Margo Workload Orchestration Agent
    - This enables the device with the functionality outlined within the Workload Orchestration Agent section of the specification
    - The Standalone Device MUST support Docker Compose file(s) for application deployment.
- Host the following additional components:
    - OCI Container Runtime 
    - OTEL Collector 
    - Policy Agent
    - Host Device Orchestration Agent 
        - **Note:** Out of scope for MVS1


    - Host Device Orchestration Agent 
        - **Note:** Out of scope for MVS1

