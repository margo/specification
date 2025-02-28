# Onboarding
In order for the Workload Fleet Management software to manage the edge device's workloads, the device's management client must first complete onboarding.

> Action: The details in this page are still under discussion and have not been finalized.

**The onboarding process includes:**

- The end user provides the the Workload Fleet Management web service's root URL to the device's management client
- The device's management client downloads the workload orchestration solution vendor's public root CA certificate using the [Onboarding API](../../margo-api-reference/workload-api/onboarding-api/rootca-download.md)
- Context and trust is established between the device's management client and the Workload Fleet Management web service
- The device's management client uses the [Onboarding API](../../margo-api-reference/workload-api/onboarding-api/device-onboarding.md) to onboard with the workload orchestration service.
- The device's management client receives the client Id, client secret and token endpoint URL used to generate a bearer token.
- The device's management client receives the URL for the Git repository containing its desired state and an associated access token for authentication
- The [device capabilities](./device-capability-reporting.md) information is sent from the device to the workload orchestration web service using the [Device API](../../margo-api-reference/workload-api/device-api/device-capabilities.md)

![Margo Management Interface Operational Flow Diagram (svg)](../../figures/margo-interface-generic.drawio.svg)
> Action: FIDO Device onboarding has not been finalized as the standard onboarding solution. Further discussion/investigations are needed. 

### Configuring the Workload Fleet Management Web Service URL

> Action: Ideally this URL is discoverable instead of having to manually enter it but we still need to determine if there is a good way to make this discoverable by using something like the FDO Rendezvous service or multicast DNS. Also, once we determine how the Margo compliant device onboarding and fleet management is going to work it will probably impact this.

To ensure the management client is configured to communicate with the correct Workload Fleet Management web service, the device's management client needs to be configured with the expected URL. The device vendor MUST provide a way for the end user to manually set the URL the device's management client uses to communicate with the workload orchestration solution chosen by the end user.

### Margo Web API Authentication Method

The Margo Web API communication pattern between the device's management client and the workload orchestration web service must use a secure communication channel. In order to facilitate this secure communication Margo requires the use of oAuth 2.0 for authentication.

#### API Authorization Strategy

- During the [onboarding process](../../margo-api-reference/workload-api/onboarding-api/device-onboarding.md) the Workload Fleet Management's web service provides the management client with a client Id, client secret and token endpoint URL
- The management client uses this information to [create a bearer token ](../../margo-api-reference/margo-api-specification.md#authorization-header)for each request
- The bearer token is set in the `Authorization` header for each web request sent to the Workload Fleet Management's web service requiring authorization.

#### Payload Security Method

> Action: Certificate Rotation / Unique Identifier for device are still research areas needed.

Because of limitations using mTLS with common OT infrastructure such as TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection Margo has adopted a certificate-based payload signing approach to protect payloads from being tampered with. By utilizing the certificates to create payload envelopes, the device's management client can ensure secure transport between the device's management client and the Workload Fleet Management's web service.

- During the onboarding process the end user uploads the device's x.509 certificate to the workload orchestration solution 
- The device's management client downloads the root CA certificate using the [Onboarding API](../../margo-api-reference/workload-api/onboarding-api/rootca-download.md)
- Once this is complete, both parties are able to [secure their payloads](../../margo-api-reference/margo-api-specification.md#signing-payloads). 

##### Details pertaining to the message Envelope:

Once the edge device has a message prepared for the Workload Fleet Management's web service, it completes the following to secure the message.

- The device's management client calculates a digest and signature of the payload
- The device's management client adds an envelope around it that has:
    - actual payload
    - SHA of the payload, signed by the device certificate
    - Identifier for the certificate that corresponds to the private key used to sign it. 
        - This identifier MUST be the GUID provided by the device manufacturer. Typically the hardware serial number. 
- The envelope is sent as the payload to the Workload Fleet Management's web service. 
- The Workload Fleet Management's web service treats the request's payload as envelope structure, and receives the certificate identifier.
> Note: This certificate is the device certificate that was manually uploaded to the workload orchestration solution during onboarding. 
- The Workload Fleet Management's web service computes digest from the payload, and verifies the signature using the device certification.
- The payload is then processed by the Workload Fleet Management's web service. 


### GitOps Service Enrollment

> Action: The Margo TWG is currently reviewing alternatives to GitOps. This page will be updated upon a finalization of a new strategy. 

#### Authorization methods for the Desired State Git Repository

- Git access tokens shall be provided to the device's management client. These access tokens MUST be tied to a dedicated non-user account for access where credentials are frequently rotated and short lived.
- Need to support accessing rotations of tokens
