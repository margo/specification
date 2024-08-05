# Workload Management Interface
The Margo Management Interface is a critical component that enables interoperability between devices and workload orchestrators. This interface MUST be supported on Margo compliant devices and orchestration services. This documentation section focuses on the Workload Management functions of the interface. The interface services can either be pre-packaged by the Device Manufacturer at production or be installed by the Device Integrator. This interface MUST be agnostic to the eventual Orchestration level vendors. 

**Workload Management Interface Requirements:**

- Margo REST API MUST be utilized for the following core functions; interface enrollment, device capabilities reporting, and deployment status updates.
- Workload Orchestration Software vendors MUST provide a Margo Compliant service endpoint to enable the API Communications.
- Open Gitops pattern MUST be utilized by the interface for Deployment specification retrieval.
- Workload Orchestration Software MUST maintain a Git Repository to store deployment specifications. This is retreived via the Edge Device's interface.
- Both API and Gitops patterns must support extended device communication downtime. 
- The Management Interface MUST reference industry security protocols and port assignments.
- Containerized Margo Interface services are prefered and enable easier lifecycle management, however, are not required.
- API Configuration Options that MUST be supported via the WOS.
	- Downtime configuration - ensures the interface is not retrying when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period. 
- GitOps Configuration Options that MUST be supported via the WOS.
	- Polling Interval Period - Describes a configurable time period when the Polling is allowed.
	- Polling Interval Rate - Describes the rate at which the WOA shall poll the repository for a new Desired State.

![Margo Management Interface for Workloads (svg)](../../figures/System-design-workload-orchestration-agent.drawio.svg)

## Margo Management Interface Generic Operations
![Margo Management Interface Operational Flow Diagram (svg)](../../figures/margo-interface-generic.drawio.svg)
