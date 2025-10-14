# Workload Fleet Management

In order to achieve Margo's interoperability mission statement, the Margo Management Interface is a critical component that enables vendor interoperability between Workload Fleet Management suppliers and Device suppliers. These suppliers are able to utilize the open implementation provided by the Margo community as is, or follow the specification to build their own compatible client/server components.

Fleet management within Margo follows a state seeking model utilizing local device providers to complete the orchestration defined via the desired state. See [Fleet Management concepts](../personas-and-definitions/technical-lexicon.md#fleet-management) for further details. 

The main goals of the management interface are as follows:

- Workload Fleet Management suppliers are able to onboard and manage workloads on all Margo compliant devices by hosting the server side of the interface.
- Device's equipped with the interface client enable any Margo compliant Fleet Management solution to manage the local workloads.

## Relevant Links

Please follow the subsequent links to view more technical information regarding Margo's management interface:

- [Margo API Technical Reference](../margo-api-reference/workload-api/api-req-security-details.md)
