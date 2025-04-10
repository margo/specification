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

An application is a collection of one, or more, [Workloads](#workload) bundled together in an [application package](../app-interoperability/application-package-definition.md).

#### Component

A Component is a piece of software tailored to run within a customer's environment on a [Edge Compute Device](#edge-compute-device). A Component within Margo consists of a description file, manifest(s), along with one or more source code containers.
Supported Component manifests include:

- Helm Chart
- Compose file

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

##### Application Registry

Service that can be used by [Application](#application) developers to make their applications available.
As of now Application Registries MUST be Git repositories.

[Workload Fleet Managers](#workload-fleet-manager) cannot access Application Registries directly, they can only access [Application Catalogs](#application-catalog).

##### Application Catalog

List of [Applications](#capplication) available for the [Workload Fleet Manager](#workload-fleet-manager) to deploy them to [Edge Compute Devices](#edge-compute-device).

An Application Catalog obtains the offered [Applications](#application) from one or more [Application Registries](#application-registry).

An Application Catalog MIGHT be optionally implemented as an [Application Registry](#application-registry).

##### Component Catalog

List of [Components](#component) within the [Workload Fleet Manager](#workload-fleet-manager) that the end user has access to deploy and manage.

#### Workload Fleet Management Client

The Workload Fleet Management Agent is a service that runs on the [Edge Compute Device](#edge-compute-device) which communicates with the [Workload Fleet Manager](#workload-fleet-manager) to receive [Components](#component) that will be instantiated as [Workloads](#workload) and configurations to be applied on the [Edge Compute Device](#edge-compute-device).

#### Device Fleet Manager

Device Fleet Manager (DFM) represents a software offering that enables End Users to onboard, delete, and maintain [Edge Compute Devices](#edge-compute-device) within the ecosystem. This software is utilized in conjunction with the [Workload Fleet Manager](#workload-fleet-manager) software to provide users with the features required to manage their [Edge Device](#edge-compute-device) along with [Workloads](#workload) running on them.  

#### Device Fleet Management Client

The Device Fleet Management Agent is a service that runs on the [Edge Compute Device](#edge-compute-device) which communicates with the [Device Fleet Manager](#device-fleet-manager) to receive device configuration to be applied on the [Edge Compute Device](#edge-compute-device).

#### Workload Marketplace

Workload Marketplace is the location where end users purchase the rights to access [Workloads](#workload) from a vendor.  

Functional Requirements of the Workload Marketplace:

- Provide users with a list of Workloads available for purchase
- Enable users to purchase access rights to a Workload
- Enable users with the meta data to access associated Workload Registries/Repositories

> Note: The Workload Marketplace component is out of scope for Project Margo. However, it is necessary to define to clarify the full user workflow.
