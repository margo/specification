# Workload Orchestration Software

The Workload Orchestration Software plays a critical role within the Margo system design. This component enables users with Workload Orchestration functions including deploying, deleting, and upgrading workloads. Although this component is out of scope for Margo, certain functionality is required from a Workload Orchestration vendor to enable the system architecture. This software interfaces with application developer repositories, vendor marketplaces, and edge devices to orchestrate the lifecycle of workloads. 

## Functional Requirements

- Application Lifecycle management
    - Deployment of Applications
    - Configure workload instances per tenant
    - Upgrades
    - Scaling
- Must provide Margo compatible communication channel and Desired state format to the Margo Compliant Workload Orchestration Agent
    - See Workload Orchestation Agent section for more details
- Edge Resource allocation and Enforcement 
- Networking configurations
- Secret management
- Volume and Storage management
- Node Management
- Policy Enforcement
- User Authentication and Security
- API/CLI interfaces
- Logging and Monitoring


> **Note**  
> The list below is not a comprehensive list and Workload Orchestration vendors are able to differentiate with additional user features. 

## Relevant Sections
- [Workload Orchestration to App Registry Interactions](../app-interoperability/workload-orch-to-app-reg-interaction.md)
- [Workload Orchestration Agent](../app-interoperability/workload-orchestration-agent.md)
