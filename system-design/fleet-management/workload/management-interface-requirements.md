# Management Interface Requirements

Provided below are a set of requirements that the Management Interface participants must follow to become Margo compliant.

- Additional technical details can be found in the following location: [Margo Management API specification](../../margo-api-reference/margo-api-specification.md)

## Requirements

- The Management Interface MUST provide the following functionality:
	- device onboarding with the workload orchestration solution
   	- device capabilities reporting
	- identifying desired state changes
	- deployment status reporting
- The Workload Fleet Management vendors MUST implement the server side of the API specification.
- The device vendor MUST implement a client following the API specification.
- The Workload Fleet Management vendors solution MUST maintain a storage repository to store the managed edge device's associated set of desired state files.
    - Margo does not dictate how the desired state files are stored, other than ensuring they are available upon request. 
- The device's management client MUST retrieve the device's set of desired state files from the Workload Fleet Manager.
- Interface patterns MUST support extended device communication downtime. 
- The Management Interface MUST MUST reference industry security protocols and port assignments for both client and server interactions.
- Running the device's management client as containerized services is preferred to enable easier lifecycle management but not required.
- The Management Interface MUST allow an end user to configure the following:
	- Downtime configuration - ensures the device's management client is not retrying communication when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period. 
	- Polling Interval Period - describes a configurable time period indicating the hours in which the device's management client checks for updates to the device's desired state.
	- Polling Interval Rate - describes the rate for how frequently the device's management client checks for updates to the device's desire state.