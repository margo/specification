# Technical Lexicon

Below are concepts and terms utilized throughout the Margo Specification along with their associated description/definition.

## Concepts

#### Interoperability

Interoperability is an overloaded term that has different meanings depending on the context. For Margo, interoperability is about achieving the following:

- Defining a common approach for packaging workloads so they can be deployed to any compatible Margo-compliant edge compute devices via any Margo-compliant workload fleet management software.
- Defining a common approach for packaging device software and firmware updates so they can be deployed to any Margo-compliant edge compute devices via any Margo-compliant device fleet management software.
- Defining a common API to enable communication between any Margo-compliant edge compute devices and any Margo-compliant fleet management software.
- Defining a common approach for collecting and transmitting diagnostics and observability data from a Margo-compliant edge compute device

#### Orchestration

Orchestration is an overloaded term that has different meanings depending on the context. For Margo, orchestration is about the delivery of workloads and device software updates to Margo-compliant edge compute devices via Margo-compliant fleet management software. Margo depends on container orchestration platforms such as Kubernetes, Docker and Podman existing on the edge compute devices and is not an attempt to duplicate what these platforms provide.

#### Fleet Management

Fleet Management represents a concept or pattern that enables users to manage one to many set of workloads and devices the customer owns. Many strategies exist within fleet management such as canary deployments, rolling deployments, and many others. Below are two fleet management concepts that have been adopted by Margo.

##### State Seeking

The state seeking methodology, adopted via Margo, is enabled first by the Workload Fleet Manager when it establishes the "Desired state". The Edge Device then reconciles it's "Current state" with the "Desired state" provided by the Fleet Manager and reports the status.

##### Provider Model

The provider model within Margo describes a service that is able to orchestrate or implement the desired state within the edge device.
Current providers supported:

- Helm Client
- Docker Compose Client

## Technical Terms

#### Application

An application is a collection of one, or more, workloads bundled together in an [application package](../app-interoperability/application-package-definition.md).

#### Workload

An Edge Workload is a piece of software tailored to run within a customer's environment on a Edge Compute Device. A Workload within Margo consists of a description file, manifest(s), along with one or more source code containers.
Supported Workload manifests include:

- Helm Package
- Docker Compose Manifest

#### Edge Compute Device

Edge Compute Devices are represented by compute hardware that runs within the customer's environment to enable the system with Margo Compliant Workloads. Edge Compute Devices host the Margo compliant management agents, container orchestration platform, and device operating systems. Margo Edge Compute Devices are defined by the roles they can facilitate within the Margo Architecture.
Supported Device roles are shown below:

- Standalone Cluster(Leader and/or Worker)
- Cluster Worker
- Standalone Device

#### Workload Fleet Manager

Workload Fleet Manager(WFM) represents a software offering that enables End Users to configure, deploy, and manage edge Workloads as a fleet on their registered Edge Devices.

##### Workload Catalog

List of Workloads within the Workload Fleet Management Software that the end user has access to deploy and manage.

#### Workload Fleet Management Agent

The Workload Fleet Management Agent is a service that runs on the Edge Compute Device which communicates with the Workload Fleet Management Software to receive workloads and configurations to be applied on the Edge Compute Device.

#### Device Fleet Manager

Device Fleet Manager(DFM) represents a software offering that enables End Users to onboard, delete, and maintain Edge Compute Devices within the ecosystem. This software is utilized in conjunction with the Workload Fleet Manager software to provide users with the features required to manage their edge device along with workloads running on them.  

#### Device Fleet Management Agent

The Device Fleet Management Agent is a service that runs on the Edge Compute Device which communicates with the Device Fleet Management Software to receive device configuration to be applied on the Edge Compute Device.

#### Workload Marketplace

Workload Marketplace is the location where end users purchase the rights to access Workloads from a vendor.  

Functional Requirements of the Workload Marketplace:

- Provide users with a list of Workloads available for purchase
- Enable users to purchase access rights to a Workload
- Enable users with the meta data to access associated Workload Registries/Repositories

> Note: The Workload Marketplace component is out of scope for Project Margo. However, it is necessary to define to clarify the full user workflow.
