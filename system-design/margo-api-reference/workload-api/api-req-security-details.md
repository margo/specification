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

### Margo Web API Authentication Method

The Margo Web API communication pattern between the device's management client and the Workload Fleet Manager web service must use a secure communication channel. In order to facilitate this secure communication Margo requires the use of oAuth 2.0 for authentication.

#### API Authorization Strategy

- During the [onboarding process](../../margo-api-reference/workload-api/onboarding-api/client-onboarding.md) the Workload Fleet Management's web service provides the management client with a client Id, client secret and token endpoint URL
- The management client uses this information to [create a bearer token ](../../margo-api-reference/workload-api/api-security-details.md#authorization-header)for each request
- The bearer token is set in the `Authorization` header for each web request sent to the Workload Fleet Management's web service requiring authorization.

### Unique Identifiers
To ensure each device's management client has a unique id, the Workload Fleet manager should produce a unique id, and present that to the user for usage at a later point. 

- This unique identifier enables onboarding and ensures proper allocation of desired state files to the appropriate client. 
- Unique identifier must be in the format of "GUID"

### Certificates
Using x.509 certificates

Onboarding certificate? 

Who is the rootCA? How do the various entities verify the authenticity of these x.509s?

#### Authorization Header
For requests requiring authentication a bearer token MUST be present in the message's `Authorization` header.

You can get the access token by sending a request to the Workload Fleet Manager web service's token URL, providing the device's client Id and secret.

```bash
curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=client_credentials&client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>" \
<WOS_Token_URL>
```
The request's response indicates the access token to use for subsequent requests.

```json
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Set the `Authorization` headers value to `Bearer <ACCESS_TOKEN>` When making request requiring authorization. For example:

```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://wos.example.com/device/2fc3d8e9-8c56-4270-b7d3-8ed30262e5e1
```

#### Payload Security Method

> Action: Certificate Rotation / Unique Identifier for device are still research areas needed.

Because of limitations using mTLS with common OT infrastructure such as TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection Margo has adopted a certificate-based payload signing approach to protect payloads from being tampered with. By utilizing the certificates to create payload envelopes, the device's management client can ensure secure transport between the device's management client and the Workload Fleet Management's web service.

- During the onboarding process the end user uploads the device's x.509 certificate to the Workload Fleet Manager solution 
- The device's management client downloads the root CA certificate using the [Onboarding API](../../margo-api-reference/workload-api/onboarding-api/rootca-download.md)
- Once this is complete, both parties are able to [secure their payloads](../../margo-api-reference/workload-api/api-security-details.md#signing-payloads). 

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

