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

## Onboarding Sequence diagram

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Server

    Note over Client,Server: 🔐 Initial Trust Establishment. 
    Note over Client,Server: This root CA certificate could alternatively been provided out of band. <br> e.g.: USB Stick, from Device Fleet management onboarding, FDO workflow.
    Client->>Server: GET /onboarding/certificate
    Server-->>Client: base64-encoded Root CA certificate
    Client-->>Client: injecting Root CA into trusted store

    Note over Client,Server: 🔒 Standard TLS Handshake Start
    Client->>Server: TLS ClientHello (TLS versions, cipher suites, random)
    Server-->>Client: TLS ServerHello (chosen version, cipher, random)
    Server-->>Client: X.509 certificate chain(server + intermediate(if applicable))
    Client-->>Client: Verifies server cert chain based on RootCA
    Note over Client,Server: 🔒 Standard TLS Handshake completed
    WFMUser->>Server: Opportunity for user to manually upload client certificate
    Note over Client,Server: Device Client onboarding begins
    Client->>Server: POST /onboarding with public_certificate (could exchange additional info)
    WFMUser->>Server: Opportunity for user to approve or reject client onboarding
    alt Public key trusted/user approved
        Note over Server: Server verifies client certificate and assigns UUID
        Server-->>Client: 201 Created { client_id }
    else Public key invalid/Client rejected
        Server-->>Client: 400 Bad Request {error: "Invalid certificate"}
        Server-->>Client: 403 Forbidden{ error: "Client rejected"}
    end
    Note over Client,Server: Device Client onboarding Ends
    Note over Client,Server: 📡 Secure API Usage with Signed Payloads can now begin

    Client->>Server: POST /client/{clientId}/capabilities
    Server-->>Client: 201 Created
    Note over Client,Server: Enrollment is complete

    Note over Client,Server: Assumed Desired state has been transmitted via WFM(out of scope for this SUP)
    Note over Client,Server: 📡 Secure API Usage with Signed Payloads
    Client->>Server: POST /client/{clientId}/deployment/{deploymentId}/status
    Server-->>Client: 201 Created
```

#### Sequence Diagram Notes
- Following Step 3: Root CA is now trusted in the TLS handshake
- Diagram depicts a standard TLS flow, but additional steps in the handshake can occur.
- (After post /onboarding) 
    - Verification of client cert out of scope of this. Pre specify
    - Step approves the client can join the server. Additional information can be tied to the certificate but are not required in this SUP. supporting information can also be transferred during this step approving this client can join the server. other things could be tied to the certificate. i.e. Cert supplied via Dell / serial number of device /
    - FDO bootstrapping off of ownership vouchers could be integrated here as well. 

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