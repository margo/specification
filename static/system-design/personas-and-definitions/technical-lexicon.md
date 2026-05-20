# Technical Lexicon

Below are concepts and terms utilized throughout the Margo Specification along with their associated description/definition.

## Concepts

#### Interoperability

Interoperability is an overloaded term that has different meanings depending on the context. For Margo, interoperability is about achieving the following:

- Defining a common approach for packaging [Components](#component) so they can be deployed as [Workloads](#workload) to any compatible Margo-compliant [Edge Compute Devices](#edge-compute-device) via any Margo-compliant [Workload Fleet Manager](#workload-fleet-manager).
- Defining a common approach for packaging device software and firmware updates so they can be deployed to any Margo-compliant [Edge Compute Devices](#edge-compute-device) via any Margo-compliant [Device Fleet Manager](#device-fleet-manager).
- Defining a common API to enable communication between any Margo-compliant [Edge Compute Devices](#edge-compute-device) and any Margo-compliant [fleet management](#fleet-management) software.
- Defining a common approach for collecting and transmitting diagnostics and observability data from a Margo-compliant [Edge Compute Device](#edge-compute-device)

#### Orchestration

Orchestration is an overloaded term that has different meanings depending on the context. For Margo, orchestration is about the deployment of [Workloads](#workload) and device software updates to Margo-compliant [Edge Compute Devices](#edge-compute-device) via Margo-compliant [fleet management](#fleet-management) software. Margo depends on container orchestration platforms such as Kubernetes, Docker and Podman existing on the [Edge Compute Devices](#edge-compute-device) and is not an attempt to duplicate what these platforms provide.

#### Fleet Management

Fleet Management represents a concept or pattern that enables users to manage one to many set of [workloads](#workload) and devices the customer owns. Many strategies exist within fleet management such as canary deployments, rolling deployments, and many others. Below are two fleet management concepts that have been adopted by Margo.

##### State Seeking

The state seeking methodology, adopted via Margo, is enabled first by the [Workload Fleet Manager](#workload-fleet-manager) when it establishes the "Desired state". The [Edge Device](#edge-compute-device) then reconciles it's "Current state" with the "Desired state" provided by the Fleet Manager and reports the status.

##### Provider Model

The provider model within Margo describes a service that is able to orchestrate or implement the desired state within the [Edge Device](#edge-compute-device).
Current providers supported:

- Helm Client
- Compose Client

## Technical Terms

#### Application

An application is a collection of one, or more, [Components](#component), as defined by an [Application Description](../specification/applications/application-description.md), and bundled within an [Application Package](#application-package).

#### Application Package

An Application Package is used to distribute an [application](#application). The parts of an Application Package are: Application Description (that refers to contained and deployable Components) as well as associated resources (e.g., icons). While the application package is made available in an [Application Registry](../concepts/applications/application-registry.md), the referenced [components](#component) are stored in a [Component Registry](#component-registry), and the linked containers are provided via a OCI [Container Image Registry](#container-image-registry).

#### Component

A Component is a piece of software tailored to be deployed within a customer's environment on an [Edge Compute Device](#edge-compute-device).
Currently Margo-supported components are:

- Helm Chart
- [Compose Archive](#compose-archive)

#### Compose Archive
A Compose Archive is a tarball file containing the Compose file, `compose.yaml`, which is formatted according the [Compose specification](https://www.compose-spec.io/), and any additional artifacts referenced by the Compose file (e.g., configuration files, environment variable files, etc.). 

#### Workload

A Workload is an instance of a [Component](#component) running within a customer's environment on a [Edge Compute Device](#edge-compute-device).

#### Edge Compute Device

Edge Compute Devices are represented by compute hardware that runs within the customer's environment to enable the system with Margo Compliant [Workloads](#workload). Edge Compute Devices host the Margo compliant management agents, container orchestration platform, and device operating systems. Margo Edge Compute Devices are defined by the roles they can facilitate within the Margo Architecture.
Supported Device roles are shown below:

- Standalone Cluster(Leader and/or Worker)
- Cluster Worker
- Standalone Device

#### Workload Fleet Manager

Workload Fleet Manager (WFM) represents a software offering that enables End Users to configure, deploy, and manage edge [Workloads](#workload) as a fleet on their registered [Edge Devices](#edge-compute-device).

##### Workload Fleet Management Client

The Workload Fleet Management client is a service that runs on the [Edge Compute Device](#edge-compute-device) which communicates with the [Workload Fleet Manager](#workload-fleet-manager) to receive [Components](#component) that will be instantiated as [Workloads](#workload) and configurations to be applied on the [Edge Compute Device](#edge-compute-device).

#### Device Fleet Manager

Device Fleet Manager (DFM) represents a software offering that enables End Users to onboard, delete, and maintain [Edge Compute Devices](#edge-compute-device) within the ecosystem. This software is utilized in conjunction with the [Workload Fleet Manager](#workload-fleet-manager) software to provide users with the features required to manage their [Edge Device](#edge-compute-device) along with [Workloads](#workload) running on them.  

> Note: The Device Fleet Manager is a future component of the Margo specification. This section will be expanded as the community defines device management functionality. 


#### Application Registry

An [Application Registry](../concepts/applications/application-registry.md) hosts [Application Packages](#application-package) that define, through their [Application Description](../specification/applications/application-description.md), the application as one or multiple [Components](#component).
It is used by application developers to make their applications available.
The [API of the Application Registry](../specification/applications/application-registry.md) is compliant with the [OCI Registry API (v1.1.0)](https://github.com/opencontainers/distribution-spec/blob/v1.1.0/spec.md).


#### Application Catalog

An Application Catalog is a visual representation of preselected, install-ready applications, the user of the [WFM](#workload-fleet-manager) can deploy to it's managed [Edge Compute Devices](#edge-compute-device). Application Catalogs and how they function within the WFM are out of scope for Margo.


#### Component Registry

A Component Registry holds [Components](#component) (e.g., Helm Charts and Compose Archives) for [Application Packages](#application-package).
When an application gets deployed through a [Workload Fleet Manager](#workload-fleet-manager), the components (linked within an [Application Description](../specification/applications/application-description.md)) are requested from the Component Registry and then deployed as [workloads](#workload). Components link to containers that are typically provided through [Container Registries](#container-image-registry).
The Component Registry can be implemented, e.g., as an OCI Registry.

#### Container Image Registry
A Container Image Registry hosts container images. [Components](#component) which are provided  as Helm Charts or Compose Archives link to such container images.
