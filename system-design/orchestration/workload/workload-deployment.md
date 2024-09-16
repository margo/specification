# Desired State Storage and Retrieval

Margo uses an [OpenGitOps](https://opengitops.dev/) approach for managing the edge device's desired state. The workload orchestration solution vendor maintains Git repositories, under their control, to push updates to the desired state for each device being managed. The device's management client is responsible for monitoring the device's assigned Git repository for any changes to the desired state that MUST be applied.
> Action: The use of GitOps patterns for pulling desired state is still being discussed/investigated. 


### Desired State Requirements:

> Note: Need to investigate best way to construct the Git Repository. Folder structure / Multiple applications per Edge Device/Cluster
> Note: this is the recommendation from FluxCD <https://fluxcd.io/flux/guides/repository-structure/>

- The workload orchestration solution MUST store the device's [desired state documents](../../margo-api-reference/workload-api/desired-state-api/desired-state.md) within a Git repository the device's management client can access. 
> Note: Git repository storage was selected to ensure secure storage and traceability pertaining to the workload's desire state(s).  
- The device's management client MUST monitor the device's Git repository for updates to the desired state using the URL and access token provided by the workload orchestration solution during onboarding.

### Workload Management Sequence of Operations

#### Desired State lifecycle:

1. The workload orchestration solution creates the [desired state documents](../../margo-api-reference/workload-api/desired-state-api/desired-state.md) based on the end user's inputs when installing, updating or deleting an application.
2. The workload orchestration solution pushes updates to the device's Git repository reflecting the changes to the desired state.
3. The device's management client monitors its assigned Git repository for changes.
4. When the device's management client notices a difference between the current (running) state and the desired state, it MUST pull down and attempt to apply the new desired state.

#### Applying the Desired State:

1. The device attempts to apply the desired state to become new current state
2. While the new desired state is being applied, the device's management client MUST report progress on state changes (see the [deployment state](#deployment-status) section below) using the [Device API](../../margo-api-reference/workload-api/device-api/deployment-status.md)

#### Deployment Status

The deployment status is sent to the workload orchestration web service using the [Device API](../../margo-api-reference/workload-api/device-api/deployment-status.md) when there is a change in the deployment state. This informs the workload orchestration web service of the current state as the new desired state is applied. 

The deployment status uses the following rules:

- The state is `Pending` once the device management client has received the updated desired state but has not started applying it. When reporting this state indicate the reason.
    - Such as waiting on Policy agent
    - Waiting on other applications in the 'Order of operations' to be completed.
- The state is `Installing` once the device management client has started the process of applying the desired state.
- The state is `Failure` if at any point the desired state fails to be applied. When reporting a `Failure` state the error message and error code MUST be reported
- The state is `Success` once the desired state has been applied completely 

![Workload Install Sequence Diagram (svg)](../../figures/workload-install-sequence.drawio.svg)
