# Deployment Specification storage and retrieval
Margo uses a GitOps style approach to manage a Edge Device's Deployment Specification and associated configuration changes. For each device the Workload Orchestration Software maintains a source code/file-based repository under its control. The Margo Management Interface is responsible for monitoring this code repository for any changes and applying the Desired State configurations.

**Deployment specification requirements:**

- The Deployment specification MUST be stored within a Git Repository available to access via the Margo Interface. Git Repository storage was selected to ensure secure storage and traceability pertaining to the Workload Desired state(s).  
- The Margo Device Interface shall have a service utilizing Open Gitops Patterns to monitor the repository via release URL, which houses the associated Deploymnt specification. 

> Note: Need to investigate best way to construct the Git Repository. Folder structure / Multiple applications per Edge Device/Cluster
> Note: this is the recommendation from FluxCD https://fluxcd.io/flux/guides/repository-structure/

## Interface - Workload Management Sequence of Operations 

**Deployment specification lifecycle:**

1. User constructs the Desired state within the WOS
2. WOS Prepares the Desired state within the Edge associated Git Repository
3. Interface monitors the Edge Device Assigned Git Repository release URL 
4. Once the interface notices a difference between the Current(running) state and Desired state, it shall pull down the new Desired state via Open Gitops methods.

**Deployment Specification being applied:**

1. Device Applies Desired state to become "Current State"
2. While applying current state, the interface shall report progress via API on state changes(see section below)

**During installation, the deployment status should be sent to the WOS via the interface. The following MUST be included.** 

- Deployment ID that matches the Deployment spec id metadata parameter. 
- Current State of the overall deployment:
	- Send overall deployment spec state(inherits the component state that is being deployed)
	- Send also individual component states

**If Pending, report information regarding the reason.**

- Such as waiting on Policy agent
- Waiting on other applications in the 'Order of operations' to be completed. 

**If Installing, report INSTALLING for whole deployment**

**If Failure, report failure condition and associated details.**

- Such as error message / error code

**If Success, report INSTALLED**


## Deployment Specification - Cluster Enabled Devices

The Deployment specification shall be formated as a Custom Resource Definition YAMl File. 

**Example Cluster Enabled Device Deployment Specification:**

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

## Deployment Specification - Standalone Devices

**Example Cluster Enabled Device Deployment Specification:**

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


**Top-level Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `ApplicationDeployment`.|
| metadata        | Metadata    | Y    | Metadata element specifying characteristics about the application deployment. |
| spec            | Spec    | Y    | Spec element that defines deployment profile and parameters associated with the application deployment. |

**Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| annotations             | Annotations          | Y    | Defines the application ID and unique identifier associated to the deployment specification. Needs to be assigned by the Workload Orchestration Software.|
| name             | string          | Y    | The application's official name. This name is for display purposes only and can container whitespace and special characters.|


**Annotation Attributes**

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| applicationId         | string          | Y    | An identifier for the application. The id is used to help create unique identifiers where required, such as namespaces. The id must be lower case letters and numbers and MAY contain dashes. Uppercase letters, underscores and periods MUST NOT be used. The id MUST NOT be more than 200 characters. The applicationId MUST match the associated application package Metadata "id" attribute. |
| id         | string          | Y    | The unique identifier UUID of the deployment specification. Needs to be assigned by the Workload Orchestration Software. |

**Spec Attributes**

| Attribute        | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| deploymentProfile           | Deployment Profile          | Y    | Section that defines deployment details including type and components.|
| parameters        | map[string][Parameter]          | Y    | Describes the configured parameters applied via the end-user.|


## Deployment Status 
The Deployment Statue update is sent via the Margo Device Interface to the WOS. The purpose of this API function is to provide status updates to the WOS while it installs the Deployment specification. This shall be static information regarding how the deployment specification was installed, for dynamic information please see the application observability section . 

Example deployment status:

```
{
    "apiVersion": "deployment.margo/v1",
    "kind": "DeploymentStatus",
    "deploymentId": "a3e2f5dc-912e-494f-8395-52cf3769bc06",
    "status": {
        "state": "pending",
        "error": {
            "code": "",
            "message": ""
        }
    },
    "components": [
        {
            "name": "digitron-orchestrator",
            "state": "pending",
            "error": {
                "code":"",
                "message":""
            }
        },
        {
            "name": "database-services",
            "state": "pending",
            "error": {
                "code": "",
                "message ": ""
            }
        }
    ]
}
```

**Top-level Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `DeploymentStatus`.|
| deploymentId    | string    | Y    | The unique identifier UUID of the deployment specification. Needs to be assigned by the Workload Orchestration Software. |
| status          | []status    | Y    | Section of the message that provides details on the overall deployment status. See Status Attributes section below for more details. |
| components      | []components    | Y    | Section of the message that provides details on the individual components of the deployment specification and their status'. |

**State Atrributes**

State attributes are assigned at the overall deployment level along with the individual component level. 
- State attribute MUST be on the following options: Pending, Installing, Installed, Failed.
- The overall deployment status MUST inherit the current component's status until it has gone through installing each component.

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| state      | string    | Y    | Current state of the overall deployment or individual component within the deployment specification depending on the current stage of deployment. |
| error      | Error    | N    | Location of the message where details regarding an installation error need to be provided. |

**Error Atrributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| code      | string    | Y    | Associated error code following a component failure during installation. |
| message   | string    | Y    | Associated error message that provides further details to the WOS about the error that was encountered. |

> Note: Need to figure out the options for error code and message. Are these to be free form?


**Components Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name      | string    | Y    | Name of the deployment component, inherited via the deployment specification |
| state     | string    | Y    | Current state of the deployment component. MUST be one of the following options: Pending, Installing, Installed, Failed |
| error     | Error    | N    | Location of the message where details regarding an installation error need to be provided. See **Error** attributes section above for more details.  |