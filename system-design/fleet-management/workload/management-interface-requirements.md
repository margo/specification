# Management Interface Requirements

Provided below are a set of requirements that the Management Interface participants must follow to become Margo compliant. 



## Requirements

- The Management Interface MUST provide the following functionality outlined within this specification:
	- onboarding of the management client
   	- device capabilities reporting
	- defining the workload(s) desired state
	- workload deployment status reporting
- The Workload Fleet Management supplier MUST implement the server side of the API specification contract.
- The Device Owner MUST implement the client side of the API specification contract.
- The Workload Fleet Management supplier's solution MUST maintain a storage repository to store the managed edge device's associated set of desired state files.
    - Margo does not dictate how the desired state files are stored, other than ensuring they are available upon request via API definition.
- The device's management client MUST retrieve the device's set of desired state files from the Workload Fleet Manager.
    - Following the retrieval of the desired state(s), the device MUST orchestrate the changes locally via the provider. 
- Following the initial upload of device capabilities from client to server, the device MUST update the WFM with an updated list of capabilities if any workload related changes occur.
- Interface patterns MUST support extended device communication downtime. 
- The Management Interface MUST allow an end user to configure the following:
	- Downtime configuration - ensures the device's management client is not retrying communication when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period. 
	- Polling Interval Period - describes a configurable time period indicating the hours in which the device's management client checks for updates to the device's desired state.
	- Polling Interval Rate - describes the rate for how frequently the device's management client checks for updates to the device's desire state.


## Suggestions

- Running the device's management client as containerized services is preferred. By following Margo application packaging guidelines, it makes the management interface easier to lifecycle manage, however this is not required.


## Relevant Links

Please follow the subsequent links to view more technical information regarding Margo's management interface:

- [Margo API Technical Reference](../../margo-api-reference/workload-api/api-security-details.md)