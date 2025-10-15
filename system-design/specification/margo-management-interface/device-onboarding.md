# Device Onboarding
In order for the Workload Fleet Management software to manage the edge device's workloads, the device's management client must first complete onboarding.

> Action: The details in this page are still under discussion and have not been finalized.

**The onboarding process includes:**

- The end user provides the the Workload Fleet Management web service's root URL to the device's management client
- The device's management client downloads the Workload Fleet Manager's public root CA certificate using the [Onboarding API](../../specification/margo-management-interface/certificate-api.md)
- Context and trust is established between the device's management client and the Workload Fleet Management web service
- The device's management client uses the [Onboarding API](../../specification/margo-management-interface/certificate-api.md) to onboard with the Workload Fleet Management service.
- The device's management client receives the client Id, client secret and token endpoint URL used to generate a bearer token.
- The device's management client receives the URL for the Git repository containing its desired state and an associated access token for authentication
> Action: The Margo TWG is currently reviewing alternatives to GitOps. This page will be updated upon a finalization of a new strategy. 
- The [device capabilities](../../concepts/workload-fleet-managers/device-capabilities.md) information is sent from the device to the WFM service using the [Device API](../../specification/margo-management-interface/device-capabilities.md)


### Configuring the Workload Fleet Management Web Service URL

> Action: Ideally this URL is discoverable instead of having to manually enter it but we still need to determine if there is a good way to make this discoverable by using something like the FDO Rendezvous service or multicast DNS. Also, once we determine how the Margo compliant device onboarding and fleet management is going to work it will probably impact this.

To ensure the management client is configured to communicate with the correct Workload Fleet Management web service, the device's management client needs to be configured with the expected URL. The device vendor MUST provide a way for the end user to manually set the URL the device's management client uses to communicate with the Workload FLeet Management solution chosen by the end user. 

### GitOps Service Enrollment

> Action: The Margo TWG is currently reviewing alternatives to GitOps. This page will be updated upon a finalization of a new strategy. 

#### Authorization methods for the Desired State Git Repository

- Git access tokens shall be provided to the device's management client. These access tokens MUST be tied to a dedicated non-user account for access where credentials are frequently rotated and short lived.
- Need to support accessing rotations of tokens

## Onboarding API Details
> Action: This API needs to be defined

### Route and HTTP Methods

```http
POST /onboarding/
```
### Request Body

TBD

### Response Body

TBD