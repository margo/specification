# Margo Edge Compute Device Details

Within Margo, devices are represented by compute hardware that runs within the customers environment to host Margo Compliant Applications. Margo Devices are defined by the roles they can facilitate within the Margo Architecture. An Edge Compute within Margo is initially referenced as a "Device" which represents the initial lifecycle stage. Once the device is onboarded within the Workload Orchestration Software, it assumes a role based on capabilities. 
Supported Device roles are shown below:

- Standalone Cluster
- Cluster Leader
- Cluster Worker
- Standalone Device
- Micro Device 

## Base Requirements for All Devices
- TPM support
- Secure Boot
- Attestation
- Zero Trust Network Access (ZTNA)

## Cluster Leader Role Details
The Cluster Leader Role within Margo describes devices that have the ability to manage the cluster of one or more worker nodes that are subscribed to this leader (itself included if applicable).  

**Cluster Leader Functional Requirements:**

- Enable control node functionality for in Kubernetes cluster 
- Support minimum set of Kubernetes control node API for a cluster leader 
- Support the "Workload Orchestration Agent" Interface for a Cluster leader 
    1.	Ability to authenticate to a repo 
- Support the telemetry API for a cluster leader 
- Support the "Policy Agent" API for a cluster leader 
- Support the "Device Orchestration Agent" API - out of scope for MVS1 


## Cluster Worker Role Details
The Cluster Worker Role within Margo describes devices that have a limited amount of compute capacity that can still run Margo Compliant Applications. This Role is orchestrated via the Cluster Leader.

**Cluster Worker Functional Requirements:**

- Enable Worker Node functionality within a Kubernetes Cluster
- Host the following additional components:
    - OCI Container Runtime 
    - OTEL Collector 
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
- Host the following additional components:
    - OCI Container Runtime 
    - OTEL Collector 
    - Policy Agent
    - Host Device Orchestration Agent 
        - **Note:** Out of scope for MVS1

