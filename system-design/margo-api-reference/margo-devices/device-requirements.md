# Device Requirements

All current device roles MUST meet the following requirements to be considered Margo compliant. These requirements ensure devices can effectively host and manage Margo compliant workloads. A device MUST support onboarding and management from only a single workload fleet manager.

All devices MUST provide the following components:
    
- A workload fleet management client
- An OCI container runtime
- An OTEL collector

## Standalone Cluster Role Requirements

Devices filling the standalone cluster role MUST provide the following additional components:

- Kubernetes orchestration platform
- Capabilities for deploying Helm charts
    

## Standalone Device Role Details

Devices filling the standalone device role MUST provide the following additional components:

- Compose compliant software as the orchestration platform
- Capabilities for deploying Compose applications


## Future Requirements

### Security Requirements

The following security requirements are not currently covered in the specification but expected to be covered in the future:

- Hardware-based security modules
- Secure boot
- Secure key storage and attestation mechanisms
- Zero trust security model

## Future Components

The following components are not currently required but are expected to be added in the future:

- A policy agent
- A device fleet management client

     




