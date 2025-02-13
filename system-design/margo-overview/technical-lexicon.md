# Technical Lexicon

**Workload**

An Edge Workload is a piece of software tailored to run within a customer's environment on a Edge Compute Device. A Workload within Margo consists of a description file, manifest(s), along with one or more source code containers.
Supported Workload manifests include:

- Helm Package
- Docker Compose Manifest

**Edge Compute Device** 

Edge Compute Devices are represented by compute hardware that runs within the customer's environment to eanble the system with Margo Compliant Workloads. Edge Compute Devices host the Margo compliant management agents, container orchestration platform, and device operating systems. Margo Edge Compute Devices are defined by the roles they can facilitate within the Margo Architecture.
Supported Device roles are shown below:

- Standalone Cluster(Leader and/or Worker)
- Cluster Worker
- Standalone Device

**Workload Fleet Manager**  

Workload Fleet Manager(WFM) represents a software offering that enables End Users to configure, deploy, and manage edge Workloads as a fleet on their registered Edge Devices.

**Workload Fleet Management Agent** 

The Workload Fleet Management Agent is a service that runs on the Edge Compute Device which communicates with the Workload Fleet Management Software to receive workloads and configurations to be applied on the Edge Compute Device.

**Device Fleet Manager**    

Device Fleet Manager(WFM) represents a software offering that enables End Users to onboard, delete, and maintain Edge Compute Devices within the ecosystem. This software is utilized in conjunction with the Workload Fleet Manager software to provide users with the features required to manage their edge device along with workloads running on them.  

**Device Fleet Management Agent** 

The Device Fleet Management Agent is a service that runs on the Edge Compute Device which communicates with the Device Fleet Management Software to receive device configuration to be applied on the Edge Compute Device.

**Workload Marketplace** 

Workload Marketplace is the location where end users purchase the rights to access Workloads from a vendor.  

Functional Requirements of the Workload Marketplace: 

- Provide users with a list of Workloads available for purchase 
- Enable users to purchase access rights to a Workload 
- Enable users with the meta data to access associated Workload Registries/Repositories

**Note**  
The Workload Marketplace component is out of scope for Project Margo. However, it is necessary to define to clarify the full user workflow.   

**Workload Catalog** 

List of Workloads within the Workload Fleet Management Software that the end user has access to deploy and manage.  
