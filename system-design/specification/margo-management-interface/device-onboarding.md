# Device Onboarding
In order for the Workload Fleet Management software to manage the edge device's workloads, the device's management client must first complete onboarding.

## Onboarding API Details

## Route and HTTP Methods

```https
POST /api/v1/onboarding
```
### Response Codes

| Code | Description |
|------|-------------|
| 201 Created | New client onboarded successfully. |
| 400 Invalid Certificate | Invalid certificate format or structure. |
| 403 Forbidden | Client certificate is not trusted or client rejected. |

## Example Response Body

```json
{
    "client_id": "<base-64 encoded UUID>"
}
```

## Onboarding Sequence

- The end user provides the the Workload Fleet Management web service's root URL to the device's management client
- The device's management client downloads the Workload Fleet Manager's public root CA certificate using the [Onboarding API](../../specification/margo-management-interface/certificate-api.md)
- Context and trust is established between the device's management client and the Workload Fleet Management web service
- The device's management client uses the [Onboarding API](../../specification/margo-management-interface/certificate-api.md) to onboard with the Workload Fleet Management service by providing it's x.509 certificate
- The device's management client receives it's unique client Id assigned via the Workload Fleet Manager
- The [device capabilities](../../concepts/workload-fleet-managers/device-capabilities.md) information is sent from the device to the WFM using the [Device API](../../specification/margo-management-interface/device-capabilities.md)

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