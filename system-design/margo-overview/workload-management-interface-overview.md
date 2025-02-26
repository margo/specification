# Workload Fleet Management

Workload Management is a critical functionality that enables deployment and maintenance of workloads that are deployed to the customers edge to enable business goals. In order to achieve Margo's interoperability mission statement, the [Margo management interface](../margo-api-reference/margo-api-specification.md) is a critical component that enables interoperability between Workload Fleet Management Software vendors and Device Vendors. Interface hosting solutions are able to utilize the open implementation provided by the Margo community as is, or follow the specification to build their own compatible client/server components.

The main goals of the management interface are as follows:

- By hosting the server side of the interface, Workload Fleet Managers are enabled with the ability to onboard and manage workloads on all Margo compliant devices.
- Device Vendors are able to build devices that include the client side of the interface which enables workload management via all Margo compliant fleet managers.

## Workload Deployment Sequence Diagram

```mermaid
sequenceDiagram
    actor EndUser
    participant WorkloadFleetManagerFrontEnd
    participant WorkloadManifestRepo
    participant WorkloadContainerRepo
    participant WorkloadFleetManager
       participant DeviceDeploymentspecificationRepo
    participant ContainerOrchestrator
    participant ContainerRuntime
    participant WorkloadManagementAgent
 
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
    activate WorkloadManagementAgent
    loop Continuous check for new deployment specifications
        WorkloadManagementAgent->>WorkloadFleetManager: Queries for new deployment spec(s)
        end
    WorkloadFleetManager->>WorkloadManagementAgent: Pulls deployment specification(s)
    WorkloadManagementAgent->>WorkloadManifestRepo: Pulls Workload Manifest(Helm)
    %% Need to include authentication to the app devs repository
    WorkloadManagementAgent->>ContainerOrchestrator: Provides Workload Manifest
    deactivate WorkloadManagementAgent
    loop
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component 1
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component 2
        ContainerOrchestrator->>ContainerRuntime: Initiates workload installation component n
        end
    ContainerRuntime->>WorkloadContainerRepo: Pulls OCI Containers
    activate WorkloadManagementAgent
    WorkloadManagementAgent->>WorkloadFleetManager: Provides Component Status Updates
    loop
        WorkloadManagementAgent->>WorkloadFleetManager: Component 1 Status update
        WorkloadManagementAgent->>WorkloadFleetManager: Component 2 Status update
        WorkloadManagementAgent->>WorkloadFleetManager: Component n Status update
        end
    WorkloadManagementAgent->>WorkloadFleetManager: Provides Full Deployment Status
    deactivate WorkloadManagementAgent
    WorkloadFleetManager->>WorkloadFleetManagerFrontEnd: Updates Web UI Full Deployment Status
    WorkloadFleetManagerFrontEnd->>EndUser: EndUser Receives Final Update
```

## Relevant Links

Please follow the subsequent links to view more technical information regarding Margo compliant devices:

- [Workload Fleet Manager Component overview](../fleet-management/workload/management-interface-requirements.md)
- [Margo API Reference](../margo-api-reference/margo-api-specification.md)
