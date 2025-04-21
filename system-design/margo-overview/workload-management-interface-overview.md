# Workload Fleet Management

Workload Management is a critical functionality that enables deployment and maintenance of workloads that are deployed to the customers edge to enable business goals. In order to achieve Margo's interoperability mission statement, the [Margo Management Interface](../margo-api-reference/margo-api-specification.md) is a critical component that enables interoperability between Workload Fleet Management Software vendors and Device Vendors. Interface hosting solutions are able to utilize the open implementation provided by the Margo community as is, or follow the specification to build their own compatible client/server components.

The main goals of the management interface are as follows:

- By hosting the server side of the interface, Workload Fleet Managers are enabled with the ability to onboard and manage workloads on all Margo compliant devices.
- Device Vendors are able to build devices that include the client side of the interface which enables workload management via all Margo compliant fleet managers.

## Workload Deployment Sequence Diagram

```mermaid
---
config:
    layout: elk


---
sequenceDiagram
    actor EndUser
    participant WorkloadFleetManagerFrontEnd
    participant WorkloadManifestRepo
    participant WorkloadContainerRepo
    participant WorkloadFleetManager
    participant DeviceDeploymentspecificationRepo
    participant ContainerOrchestrator
    participant ContainerRuntime
    participant WorkloadFleetManagementClient
 
    autonumber
    EndUser->>WorkloadFleetManagerFrontEnd: Visits App Catalog Page
    WorkloadFleetManagerFrontEnd->>WorkloadFleetManager: Get list of available workloads
    activate WorkloadFleetManager
    WorkloadFleetManager->>WorkloadFleetManagerFrontEnd: Return
    deactivate WorkloadFleetManager
    EndUser->>WorkloadFleetManagerFrontEnd: Select workload to install
    WorkloadFleetManagerFrontEnd->>WorkloadFleetManager: Get list of devices
    activate WorkloadFleetManager
    WorkloadFleetManager-->>WorkloadFleetManager: Filter devices on capability match
    WorkloadFleetManager->>WorkloadFleetManagerFrontEnd: Return Compatible devices
    deactivate WorkloadFleetManager
    EndUser->>WorkloadFleetManagerFrontEnd: Select Device(s) to install application on
    EndUser->>WorkloadFleetManagerFrontEnd: Answer configurable questions to be applied to workload(s)
    WorkloadFleetManager-->>WorkloadFleetManager: Create & Store new deployment specification(s)
    activate WorkloadFleetManagementClient
    loop Continuous check for new deployment specifications
        WorkloadFleetManagementClient->>WorkloadFleetManager: Queries for new deployment spec(s)
        end
    WorkloadFleetManager->>WorkloadFleetManagementClient: Pulls deployment specification(s)
    WorkloadFleetManagementClient->>WorkloadManifestRepo: Pulls Workload Manifest(Helm)
    %% Need to include authentication to the app devs repository
    WorkloadFleetManagementClient->>ContainerOrchestrator: Provides Workload Manifest
    deactivate WorkloadFleetManagementClient
    loop
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component 1
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component 2
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component n
        end
    ContainerRuntime->>WorkloadContainerRepo: Pulls OCI Containers
    activate WorkloadFleetManagementClient
    WorkloadFleetManagementClient->>WorkloadFleetManager: Provides Component Status Updates
    loop
        WorkloadFleetManagementClient->>WorkloadFleetManager: Component 1 Status update
        WorkloadFleetManagementClient->>WorkloadFleetManager: Component 2 Status update
        WorkloadFleetManagementClient->>WorkloadFleetManager: Component n Status update
        end
    WorkloadFleetManagementClient->>WorkloadFleetManager: Provides Full Deployment Status
    deactivate WorkloadFleetManagementClient
    WorkloadFleetManager->>WorkloadFleetManagerFrontEnd: Updates Web UI Full Deployment Status
    WorkloadFleetManagerFrontEnd->>EndUser: EndUser Receives Final Update
```

## Relevant Links

Please follow the subsequent links to view more technical information regarding Margo compliant devices:

- [Workload Fleet Manager Component overview](../fleet-management/workload/management-interface-requirements.md)
- [Margo API Reference](../margo-api-reference/margo-api-specification.md)
