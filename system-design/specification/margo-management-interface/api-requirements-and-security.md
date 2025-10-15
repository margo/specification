# API Requirements and Security Details
## General Requirements
- The Workload Fleet Management supplier MUST implement the server side of the API specification contract.
- The Device Owner MUST implement the client side of the API specification contract.

Below is a breakdown of the three major categories these requirements fall under:

1. Basic functions for supporting the Management Interface
    - Onboarding of the management interface client
2. Workload management functions
    - Set workload(s) desired state
    - Report the workload's deployment status 
3. Device or Client Specific Functions
    - Device Bootstrap (To be further defined by Margo)
    - Device Onboarding (To be further defined by Margo)
    - Device Software Runtime Management (To be further defined by Margo)
    - Device Capability Reporting

## Basic functions for supporting the Management Interface
### Onboarding of the Management Interface Client
> Note: This section will be completed in a future SUP submission.
#### Support for Extended Device Communications Downtime
- Interface patterns MUST support extended device communication downtime. 
- The Management Interface MUST allow an end user to configure the following:
	- Downtime configuration - ensures the device's management client is not retrying communication when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period. 
	- Polling Interval Period - describes a configurable time period indicating the hours in which the device's management client checks for updates to the device's desired state.
	- Polling Interval Rate - describes the rate for how frequently the device's management client checks for updates to the device's desire state.
- Running the device's management client as containerized services is preferred. By following Margo application packaging guidelines, it makes the management interface easier to lifecycle manage, however this is not required.

## API Security Requirements
> Note: The content documented below is still being finalized within the community, SUP process will be started shortly to finalize. 
### Margo Web API Authentication Method
The Margo Web API communication pattern between the device's management client and the Workload Fleet Manager web service must use a secure communication channel. 
### Authentication and Authorization using Certificates
> Note: This section will be completed in a future SUP submission.
### Unique Identifiers for the Workload Fleet Manager and Device's Management Interface Relationship
> Note: This section will be completed in a future SUP submission.
### Payload Security Method
> Action: Certificate Rotation (CRLs) / Unique Identifier for device are still research areas needed.

Due to the limitations of utilizing mTLS with common OT infrastructure components, such as TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection, Margo has adopted a certificate-based payload signing approach to protect payloads from being tampered with. By utilizing the certificates to create payload envelopes, the device's management client can ensure secure transport between the device's management client and the Workload Fleet Management's web service.
#### Details pertaining to the message Envelope:
Once the edge device has a message prepared for the Workload Fleet Management's web service, it completes the following to secure the message.

- The device's management client calculates a digest and signature of the payload
- The device's management client adds an envelope around it that has:
    - actual payload
    - SHA of the payload, signed by the device certificate
    - Identifier for the certificate that corresponds to the private key used to sign it. 
        - This identifier MUST be the UUID provided by the WFM server. 
- The envelope is sent as the payload to the Workload Fleet Management's web service. 
- The Workload Fleet Management's web service treats the request's payload as envelope structure, and receives the certificate identifier.
> Note: This certificate is the device certificate that was manually uploaded to the Workload Fleet Manager solution during onboarding. 
- The Workload Fleet Management's web service computes digest from the payload, and verifies the signature using the device certification.
- The payload is then processed by the Workload Fleet Management's web service.
#### Signing Payloads
The following steps are used to sign a payload:

1. Generate a SHA-256 hash value for the request's body
2. Create a digital signature by using the message source certificates's private key to encrypt the the hash value
3. Base-64 encode the certificate's public key and the digital signature in the format of `<public key>;<digital signature>`
3. Include the base-64 encoded string in the request's `X-Payload-Signature` header
### Verifying Signed Payloads
The following steps are used to verify signed payload:

1. Retrieve the public key from the `X-Payload-Signature` header
2. Decrypt the digital signature using the public key to get the original hash value
3. Generate a SHA-256 hash value for the requests's body
4. Ensure the generated hash value matches the hash value from the message
