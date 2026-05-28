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

### Helm deployment approaches

Applications can be deployed as Helm charts using either Helm [version 3](https://helm.sh/docs/v3/topics/charts) or [version 4](https://helm.sh/docs/topics/charts) using Chart APIVersion v2 only.

Margo does not dictate how devices deploy workloads packaged as Helm charts. A device vendor may choose a deployment approach that either interacts with the Kubernetes API (such as `helm install`) or an approach that renders the helm templates and applies the templates (such as `helm template` or Kustomization). In order to facility this choice, certain Helm functions are not support. See the [Helm exceptions](../applications/application-description.md#helm-exceptions) for more details.

#### Probationary support for `.Capabilities.APIVersions.Has` function

**Feedback Wanted:** We are looking for feedback on supporting this function. If you are using a deployment method that does not support passing the list of Kubernetes APIs out of band, please let us know.

If a device vendor chooses a deployment approach that does not interact with the Kubernetes API, the list of Kuberentes APIs available in the cluster MUST be provided out-of-band. This is supported by a variety of tooling such as the Helm GO SDK, `helm template` command, Kustomization, and ArgoCD.


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

     




