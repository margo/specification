# Workload Management Interface Onboarding
In order for the Workload Orchestration Software to manage the Edge Device's workloads, the Workload Management Interface must first be onboarded.

**Onboarding process includes:**

1. Margo Interface receives WOS API Endpoint and Signing Certificate HTTP Endpoint
2. Context and Trust is established between Interface and the WOS API Endpoints
3. Margo Interface receives Git release URL endpoint and interface associated access token
3. Trust establishment between the interface and the Device's Associated Git Repository 
4. Device Capability information transfer from Device to Orchestration Software

## Management Endpoint Discovery/Configuration

To ensure the Management Interface is configured to communicate with the correct API Endpoint. We need to ensure the endpoint is first configured. 

- Tier 1 Device management scenario

In this scenario the Margo interface is not aware of the WOS API Endpoint. It will either need to be configured manually or via the proprietary device management service. This scenario is also relevant for "Split-Brain" scenarios where the WOS and DOS are provided via different vendors. 

- Tier 2 Device Management scenario

It is assumed during the device onboarding process, the Management Interface endpoint will be configured automatically. Endpoint configuration MUST be a feature of the DOS.   

> Note: maybe discoverable means will need to be necessary. Rendevous server or DNS route.

## Rest API Authentication Method

The REST API communication pattern between the Management Interface and the WOS API Endpiont needs to be a secure communication channel. Due to this requirement, Margo has adopted a certificate-based authentication approach. By utilizing the certificates to create Payload Envelopes, the management interface can ensure secure transport even if there is a TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection.

API Authorization Strategy

1. End user uploads the x.509 device certificate to the WOS 
2. WOS prepares a signing certificate available via a HTTP API 
3. Edge Device Interface retrieves the signing certificate from endpoint outlined above, and traces back to the root CA to validate WOS ownership. 
4. Once this is complete, both sides of the interface are able to produce the envelope. 

Details pertaining to the message Envelope:

Once Edge Device has a message prepared for the WOS, it completes the following to secure the message.

1. Calculates a digest and signature of the payload
2. Adds envelope around it that has:
    - actual payload
    - SHA of the payload, signed by the device certificate
    - Identifier for the certificate that corresponds to the private key used to sign it. 
        - This identifier MUST be the GUID provided by the Device Manufacturer. Typically the hardware serial number. 
3. Envelope is sent as the payload to the WOS API Endpoint. 
4. WOS treats the POST payload as envelope structure, and receives the certificate identifier. Note: This certificate is the Device Certificate that was manually uploaded to the WOS. 
5. WOS computes digest from the payload, and verifies the signature using the device certification.
6. Payload is then processed via the WOS. 

> Note: Certificate Rotation / Unique Identifier for device are still research areas needed. 

## Gitops Service Enrollment

Authorization methods for OpenGitops

- Github Access Tokens shall be provided to the Management Interface. These access tokens MUST be tied to a dedicated non-user account for access where credentials are frequently rotated and short lived.
- Need to support accessing rotations of tokens

> Note: Need to think through a process for retrieving new tokens when one expires.
> Note: Is time synchronization required in this interface?