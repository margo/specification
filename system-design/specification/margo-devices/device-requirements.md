# Device Requirements

A device MUST meet a baseline set of requirements to be considered Margo-conformant. These requirements ensure devices can effectively manage Margo-conformant workload and/or host those workloads. A device MUST support onboarding and management from only a single workload fleet manager. A device reports what it can provide to the ecosystem through its [device capabilities](../margo-management-interface/device-capabilities.md).

All Margo-conformant devices MUST provide the following components:

- A workload fleet management client

> Note: This is not required for a device behind a see-thru gateway.

All workload hosting devices MUST provide the following capabilities:
    
- At least one supported deployment type
- At least one supported workload runtime
- An OTEL collector

> Note: See [device capabilities](../margo-management-interface/device-capabilities.md) for the supported deployment types and runtimes. 

## Helm-enabled Device Requirements

Devices supporting the Helm deployment type, MUST provide the following additional components:

- Capabilities for deploying Helm charts
- Kubernetes orchestration platform

### Helm deployment approaches

Applications can be deployed as Helm charts using either Helm [version 3](https://helm.sh/docs/v3/topics/charts) or [version 4](https://helm.sh/docs/topics/charts) using Chart APIVersion v2 only.

Margo does not dictate how devices deploy workloads packaged as Helm charts. A device vendor may choose a deployment approach that either interacts with the Kubernetes API (such as `helm install`) or an approach that renders the helm templates and applies the templates (such as `helm template` or Kustomization). In order to facility this choice, certain Helm functions are not support. See the [Helm exceptions](../applications/application-description.md#helm-exceptions) for more details.

#### Probationary support for `.Capabilities.APIVersions.Has` function

**Feedback Wanted:** We are looking for feedback on supporting this function. If you are using a deployment method that does not support passing the list of Kubernetes APIs out of band, please let us know.

If a device vendor chooses a deployment approach that does not interact with the Kubernetes API, the list of Kuberentes APIs available in the cluster MUST be provided out-of-band. This is supported by a variety of tooling such as the Helm GO SDK, `helm template` command, Kustomization, and ArgoCD.


## Compose-enabled Device Requirements

Devices supporting the Compose deployment type, MUST provide the following additional components:

- Capabilities for deploying Compose applications
- An OCI container runtime, for example Docker or Podman


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

     




