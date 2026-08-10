# Custom Runtimes and Deployments

Application suppliers may require a way to package and deploy applications using a deployment type or runtime that goes beyond what is defined in the Margo specification.

The functionality is supported via custom runtime and deployment types and may be used for collaboration between application and device suppliers to deploy non-Margo standardized workloads.

While custom runtime and deployment types are not interoperable by nature, a standardized mechanism ensures that such extensibility concerns do not break interoperability or conformance for other suppliers, that unknown runtime and deployment types are safely ignored, and that the Margo specification can evolve without breaking supplier-specific use cases.

The use of custom runtimes and deployment types adds functionality that is not part of the Margo specification. It is expected that suppliers collaborate in order to know what is available. Margo does not maintain a listing of these custom runtime or deployment type labels.

For specifics, see the documentation for each of the following documents:

- [Application Description](../applications/application-description.md#custom-runtimes-and-deployments)
- [Device Capabilities](../margo-management-interface/device-capabilities.md#custom-runtimes-and-deployments)
- [Application Deployment](../margo-management-interface/desired-state#deviceconstraints-attributes)

Application suppliers MUST follow the same pattern established for officially supported deployment types and use an OCI blob to package their application artifacts and use the existing Application Description [component properties](../applications/application-description#componentproperties-attributes) to describe its location. The specific details for how this OCI blob gets created (e.g. metadata, layers, contents) are the responsibility of the suppliers to agree upon and are outside the scope of Margo's specification.

Device suppliers supporting a custom runtime or deployment type MUST follow the [Device Capabilities](../margo-management-interface/device-capabilities.md#custom-runtimes-and-deployments) guidelines to report these capabilities.

## Example use case: Custom deployment of Hyper-V virtual machines via Margo

AppForge Dynamics is a company that builds security and monitoring applications. Their applications are Windows-based and can be deployed via virtual machine images that target Hyper-V.

AppForge Dynamics has partnered with two companies, EdgeCircuit Systems and NanoEdge Devices, that will supply Windows servers that can be used to deploy AppForge Dynamics virtual machines.

AppForge Dynamics has agreed to follow the Margo application package approach to package their virtual images inside an OCI blob and use the Margo Application description to make their application available. EdgeCircuit Systems and NanoEdge Devices both have Windows servers that are running their own implementation of the Margo WFM client. While they cannot deploy applications targeting Kubernetes or Compose, they can deploy AppForge Dynamics's apps.

It should be possible for these three vendors to collaborate and deploy these virtual machines to the targeted devices supplied by EdgeCircuit Systems and NanoEdge Devices. They should be able to do this using implementations based on the Margo specification while using a WFM that knows nothing about what these three suppliers are doing. There are no expectations that these VMs will be deployed on any other Margo-conformant devices except those provided by these two device suppliers. There are no expectations that these devices will be able to deploy anything but these VMs.

##### Application Description

```yaml
apiVersion: margo.org/v1-alpha1
kind: ApplicationDescription
metadata:
  id: com.appforge-dynamics.sys-sec-mon
  name: System and Security Monitoring
  description: System and Security Monitoring Application for Windows
  version: "1.0"
  catalog:
    application:
      icon: ./resources/logo.png
      tagline: Intuitive system and security monitoring.
      descriptionFile: ./resources/description.md
      releaseNotes: ./resources/release-notes.md
      licenseFile: ./resources/license.pdf
      site: http://appforge-dynamics.com/monitoring
      tags: ["monitoring", "Security", "Hyper-V", "Windows"]
    organization:
      - name: AppForge Dynamics
        site: http://appforge-dynamics.com
deploymentProfiles:
  - type: custom
    id: com.appforge-dynamics.sys-sec-mon.hyperv
    components:
      - name: sys-sec-mon
        properties:  
          repository: oci://apppforge-dynamics.azurecr.io/hyperv/sys-sec-mon
          revision: 1.0.0
    deviceConstraints:
      capacityRequirements:
        cpu:
          cores: 1
        memory: 1024Mi
        storage: 5Gi
      eligibilityRules:
        - propertySelector:
            matchExpressions:
            - key: /vendor
              operator: In
              values:
              - "EdgeCircuit Systems"
              - "NanoEdge Devices"
          labelSelector:
            matchExpressions:
            - key: example.com/hyper-v.host
              operator: In
              values:
              - true
parameters: ...
configuration: ...
```

##### Device Capabilities

```json
{
    "apiVersion": "device.margo.org/v1alpha1",
    "kind": "DeviceCapabilitiesManifest",
    "properties": {
        "id": "com.edge-circuit-systems.hardware.G12",
        "vendor": "EdgeCircuit Systems",
        "modelNumber": "EF1.234.32",
        "serialNumber": "SN12928342125",
        "memory": "64 Gi",
        "storage": "1862 Gi",
        "peripherals": [],
        "interfaces": [],
        "otelCollector": true,
        "supportedRuntimes": ["custom"],
        "supportedDeploymentTypes": ["custom"]
    },
    "labels": {
      "example.com/hyper-v.host": true 
    }
}
```