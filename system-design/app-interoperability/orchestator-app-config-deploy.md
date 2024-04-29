# Workload Orchestrator Configures Application Instance and Deploys
The Workload Orchestration Software GUI provides the user with the ability to config, install, update, or remove applications on nodes within their environment.

The Workload Orchestration Software should make use of the node resource information and the resource constraints defined in the application’s YAML files to identify any nodes in the end user’s environment the application can be installed on.

Before installing the application onto a node, the end user must be given an opportunity to configure any defined application variables. 
When the end user confirms the deployment of the new, or updated application, or removes an application, the Workload Orchestration Software updates the Node Configuration Repository with the new desired state.

The Workload Orchestration Agent monitors the Node Configuration Repository for changes to the desired state and applies the updates.
While the updates are being applied the Workload Orchestration Agent reports the current state back to the Workload Orchestration Software and the final state (success or failures) once the update is completed.  

If the application was successfully deployed the Workload Orchestration Agent reports back the latest node resource information. 

![Application Configuration and Deployment (svg)](../figures/Workload-orchestrator-app-config-deploy.drawio.svg)

## Configuration and Deployment User Workflow
- The end users select an application to install from the Workload Orchestration Software vendor’s GUI. 
- The Workload Orchestration Software identifies all Devices the application is compatible with.
- The End User selects the compatible Device to deploy the application onto.
- If applicable, the Workload Orchestration Software GUI presents the End User with a view allowing them to modify the configured variables values.
- The End User confirms the deployment.
- The Workload Orchestration Software updates the Device Configuration Repository with the new Desired State.
- The Workload Orchestration Agent, while polling the WOS for Device updates, notices a new Desired state associated to it's enrolled Device.
- The Agent then pulls down the Desired state.
- During the installation, the Decice is pointed to the associated Application Repository referenced within the Desired state. This is the location where the Helm chart or Docker compose file is located. 
- Once the install attempt completes the Workload Orchestration Agent reports back either a success or failure as the Install State.
