# API Requirements and Security Details
## Requirements

Provided below are a set of requirements that the Management Interface participants must follow to become Margo compliant. 

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
- Running the device's management client as containerized services is preferred. By following Margo application packaging guidelines, it makes the management interface easier to lifecycle manage, however this is not required.
    - Note: This requirement is a suggestion but not required via Margo conformance. 

## Authorization and Security Details
> Note: The content documented below is still being finalized within the community, SUP process will be started shortly to finalize. 

### Certificates
The following certificate strategies are utilized within the Margo Management Interface. 

- Device Client and WFM server both are represented by an x.509 certificates
    - PEM certificate format MUST be used 
- These certificates are each manually placed in the counterpart's system to enable the onboarding process detailed below. 

### Unique Identifiers
To ensure each device's management client has a unique id, the Workload Fleet manager should produce a UUID per interface client. 

- This unique identifier is produced during onboarding and enables authorization to specific content per client.  
    - Unique identifier MUST be in the format of Universally Unique Identifier(UUIDv4)

### Onboarding of the Management Interface Client

- During the onboarding process the end user uploads the WFM and device's x.509 certificates manually to their respective services. 
> Note: The Margo community is investigating solutions that will automate this process. Future updates will be completed.
- Device sends a CSR with its public key inside, and a signature in the CSR itself.
- Server extracts the public key, and verifies with it's internal authorized list.
- Server then verifies the identity of the device via a challenge via sending a nonce.
- Following a successful challenge, the WFM server provides client with the following details:
    - Status of the onboarding (Success / fail)
    - UUID associated with the device's x.509 certificate
    - JWT token
- Once this is complete, both parties are able to [signing payloads](#signing-payloads). 

> Note: For further details regarding the onboarding, please see [device onboarding](../workload-api/onboarding-api/device-onboarding.md)

## Margo Web API Authentication Method

The Margo Web API communication pattern between the device's management client and the Workload Fleet Manager web service must use a secure communication channel. 

#### API Authorization Strategy

- During the [onboarding process](../../margo-api-reference/workload-api/onboarding-api/device-onboarding.md) the Workload Fleet Management's web service provides the management client with a UUID and JWT token. 
- The JWT token is set in the `Authorization` header for each web request sent to the Workload Fleet Management's web service requiring authorization.

#### Authorization Header
For requests requiring authentication a JWT token MUST be present in the message's `Authorization` header.This token is provided by the WFM during the onboarding process. 

Set the `Authorization` headers value to `Bearer <JWT>` When making request requiring authorization. 

#### Payload Security Method

> Action: Certificate Rotation / Unique Identifier for device are still research areas needed.

Because of limitations using mTLS with common OT infrastructure such as TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection Margo has adopted a certificate-based payload signing approach to protect payloads from being tampered with. By utilizing the certificates to create payload envelopes, the device's management client can ensure secure transport between the device's management client and the Workload Fleet Management's web service.

##### Details pertaining to the message Envelope:

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

##### Signing Payloads

The following steps are used to sign a payload

1. Generate a SHA-256 hash value for the request's body
2. Create a digital signature by using the message source certificates's private key to encrypt the the hash value
3. Base-64 encode the certificate's public key and the digital signature in the format of `<public key>;<digital signature>`
3. Include the base-64 encoded string in the request's `X-Payload-Signature` header

##### Verifying Signed Payloads

The following steps are used to verify signed payloads

1. Retrieve the public key from the `X-Payload-Signature` header
2. Decrypt the digital signature using the public key to get the original hash value
3. Generate a SHA-256 hash value for the requests's body
4. Ensure the generated hash value matches the hash value from the message

