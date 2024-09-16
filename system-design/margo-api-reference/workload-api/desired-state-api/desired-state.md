# Desired State

> Action: This is incomplete and doesn't contain the details for the deploymentProfile or parameters

> Action: We are currently investigating the best way to interface with source control infrastructure.

The desired state is expressed as a [Kubernetes custom resource definition](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and made available to the device's management client as a YAML document using the OpenGitOps pattern.

### ApplicationDeployment Definition

```yaml
apiVersion: application.margo.org/v1alpha1
kind: ApplicationDeployment
metadata:
  annotations:
    id: 
    applicationId: 
  name: 
  namespace: 
spec:
    deploymentProfile:
        type: 
        components:
            - name: 
              properties:
    parameters:
        param:
            value: 
            targets:
                - pointer: 
                  components:[]
```

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `ApplicationDeployment`.|
| metadata        | Metadata    | Y    | Metadata element specifying characteristics about the application deployment. See the [Metadata Attributes](#metadata-attributes) section below. |
| spec            | Spec    | Y    | Spec element that defines deployment profile and parameters associated with the application deployment. See the [Spec Attributes](#spec-attributes) section below.|

#### Metadata Attributes

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| annotations             | Annotations          | Y    | Defines the application ID and unique identifier associated to the deployment specification. Needs to be assigned by the Workload Orchestration Software. See the [Annotation Attributes](#annotation-attributes) section below.|
| name             | string          | Y    | When deploying to Kubernetes, the manifests name. The name is chosen by the workload orchestration vendor and is not displayed anywhere.|
| namespace        | string          | Y    | When deploying to Kubernetes, the namespace the manifest is added under. The namespace is chosen by the workload orchestration solution vendor.

#### Annotation Attributes

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| applicationId         | string          | Y    | An identifier for the application. The id is used to help create unique identifiers where required, such as namespaces. The id must be lower case letters and numbers and MAY contain dashes. Uppercase letters, underscores and periods MUST NOT be used. The id MUST NOT be more than 200 characters. The applicationId MUST match the associated application package Metadata "id" attribute. |
| id         | string          | Y    | The unique identifier UUID of the deployment specification. Needs to be assigned by the Workload Orchestration Software. |

#### Spec Attributes

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| deploymentProfile           | Deployment Profile          | Y    | Section that defines deployment details including type and components.|
| parameters        | map[string][Parameter]          | Y    | Describes the configured parameters applied via the end-user.|


### Example: Cluster Enabled Application Deployment Specification

```
apiVersion: application.margo.org/v1alpha1
kind: ApplicationDeployment
metadata:
    annotations:
        applicationId: com-northstartida-digitron-orchestrator
        id: a3e2f5dc-912e-494f-8395-52cf3769bc06
    name: com-northstartida-digitron-orchestrator-deployment
    namespace: margo-poc
spec:
    deploymentProfile:
        type: helm.v3
        components:
            - name: database-services
              properties:
                repository: oci://quay.io/charts/realtime-database-services
                revision: 2.3.7
                timeout: 8m30s
                wait: "true"
            - name: digitron-orchestrator
              properties:
                repository: oci://northstarida.azurecr.io/charts/northstarida-digitron-orchestrator
                revision: 1.0.9
                wait: "true"
    parameters:
        adminName:
            value: Some One
            targets:
                - pointer: administrator.name
                  components:
                    - digitron-orchestrator
        adminPrincipalName:
            value: someone@somewhere.com
            targets:
                - pointer: administrator.userPrincipalName
                  components:
                    - digitron-orchestrator
        cpuLimit:
            value: "4"
            targets:
                - pointer: settings.limits.cpu
                  components:
                    - digitron-orchestrator
        idpClientId:
            value: 123-ABC
            targets:
                - pointer: idp.clientId
                  components:
                    - digitron-orchestrator
        idpName:
            value: Azure AD
            targets:
                - pointer: idp.name
                  components:
                    - digitron-orchestrator
        idpProvider:
            value: aad
            targets:
                - pointer: idp.provider
                  components:
                    - digitron-orchestrator
        idpUrl:
            value: https://123-abc.com
            targets:
                - pointer: idp.providerUrl
                  components:
                    - digitron-orchestrator
                - pointer: idp.providerMetadata
                  components:
                    - digitron-orchestrator
        memoryLimit:
            value: "16384"
            targets:
                - pointer: settings.limits.memory
                  components:
                    - digitron-orchestrator
        pollFrequency:
            value: "120"
            targets:
                - pointer: settings.pollFrequency
                  components:
                    - digitron-orchestrator
                    - database-services
        siteId:
            value: SID-123-ABC
            targets:
                - pointer: settings.siteId
                  components:
                    - digitron-orchestrator
                    - database-services
```

### Example: Standalone Device Application Deployment Specification:

```
apiVersion: application.margo.org/v1alpha1
kind: ApplicationDeployment
metadata:
    annotations:
        applicationId: com-northstartida-digitron-orchestrator
        id: ad9b614e-8912-45f4-a523-372358765def
    name: com-northstartida-digitron-orchestrator-deployment
    namespace: margo-poc
spec:
    deploymentProfile:
        type: docker-compose
        components:
            - name: digitron-orchestrator-docker
              properties:
                keyLocation: https://northsitarida.com/digitron/docker/public-key.asc
                packageLocation: https://northsitarida.com/digitron/docker/digitron-orchestrator.tar.gz
    parameters:
        adminName:
            value: Some One
            targets:
                - pointer: ENV.ADMIN_NAME
                  components:
                    - digitron-orchestrator-docker
        adminPrincipalName:
            value: someone@somewhere.com
            targets:
                - pointer: ENV.ADMIN_PRINCIPALNAME
                  components:
                    - digitron-orchestrator-docker
        idpClientId:
            value: 123-ABC
            targets:
                - pointer: ENV.IDP_CLIENT_ID
                  components:
                    - digitron-orchestrator-docker
        idpName:
            value: Azure AD
            targets:
                - pointer: ENV.IDP_NAME
                  components:
                    - digitron-orchestrator-docker
        idpProvider:
            value: aad
            targets:
                - pointer: ENV.IDP_PROVIDER
                  components:
                    - digitron-orchestrator-docker
        idpUrl:
            value: https://123-abc.com
            targets:
                - pointer: ENV.IDP_URL
                  components:
                    - digitron-orchestrator-docker
        pollFrequency:
            value: "120"
            targets:
                - pointer: ENV.POLL_FREQUENCY
                  components:
                    - digitron-orchestrator-docker
        siteId:
            value: SID-123-ABC
            targets:
                - pointer: ENV.SITE_ID
                  components:
                    - digitron-orchestrator-docker
```

