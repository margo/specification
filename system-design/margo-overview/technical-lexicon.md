# Technical Lexicon

**Application**

An Edge Application is a piece of software tailored to run within a customer's environment on a Edge Compute Device. The Edge Application consists of an application manifest, application description file, along with one or more containers, where the containers can be deployed on one or more nodes. 

**Edge Compute Device** 

Edge Compute Devices are represented by compute hardware that runs within the customer's environment to host Margo Compliant Applications. Margo Compute Devices are defined by the roles they can facilitate within the Margo Architecture. An Edge Compute within Project Margo is initially referenced as a "Device" which represents the initial lifecycle stage. Once the device is onboarded within the Workload Orchestration Software, it assumes a role based on capabilities. 
Supported Device roles are shown below:

- Standalone Cluster(Leader and/or Worker)
- Cluster Worker
- Standalone Device

**Workload Orchestration Software**  

Workload Orchestration Software (WOS) is the service that enables End Users to configure, deploy, and manage edge applications. Interfaces with Margo compliant App and Device registry and repositories. Complies with all Margo Functional/Non-Functional requirements for workload management. Interfaces with Margo compliant Edge device/nodes. 

**Workload Orchestration Agent** 

The Workload Orchestration Agent is a service that runs on the Edge Compute Device which communicates with the Workload Orchestration Software to receive workloads and configurations to be applied on the Edge Compute Device.

**Device Orchestration Software**    

Device Orchestration Software provides Margo with a central location to onboard, delete, and maintain Edge Compute Devices within the ecosystem. This software is utilized in conjunction with the Workload Orchestration software to provide users with the features required to manage their edge device along with workloads running on them.  

**Device Orchestration Agent** 

The Device Orchestration Agent is a service that runs on the Edge Compute Device which communicates with the Device Orchestration Software to receive device configuration to be applied on the Edge Compute Device.

**Application Registry** 

Curated access-controlled storage location where Application manifests and associated marketplace data are hosted via the Application Developer.  

**Application Repository** 

Orchestration Software typically sources Apps from Application repositories when deploying and maintaining apps on Edge Compute Devices. 

**Application Marketplace** 

Application Marketplace is the location where end users purchase the rights to access applications from a vendor.  

Functional Requirements of the Application Marketplace: 

- Provide users with a list of applications available for purchase 
- Enable users to purchase the rights to an application 
- Enable users with the meta data to access associated Application Registries/Repositories

**Note**  
The Application Marketplace component is out of scope for Project Margo. However, it is necessary to define to clarify the full user workflow.   

**Application Catalog** 

List of Applications within the Workload Orchestration Software that the end user has access to deploy and manage.  
