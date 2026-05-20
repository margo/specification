# Device Client Onboarding
In order for the Workload Fleet Management software to manage the edge device's workloads, the device's management client must first complete onboarding.

- Requests to this endpoint MUST be authenticated using the HTTP Message Signature method as defined in the [Payload Security](../margo-management-interface/api-requirements-and-security.md#payload-security-method) section.

## Onboarding Sequence

- The end user provides the the Workload Fleet Management web service's root URL to the device's management client
- The device's management client downloads the Workload Fleet Manager's public root CA certificate using the [Certificate API](../../specification/margo-management-interface/certificate-api.md)
- Context and trust is established between the device's management client and the Workload Fleet Management web service
- The device's management client uses the [Onboarding API](../../specification/margo-management-interface/device-client-onboarding.md) to onboard with the Workload Fleet Management service by providing its X.509 certificate
- The device's management client receives its unique client Id assigned via the Workload Fleet Manager
- The [device capabilities](../../concepts/workload-fleet-managers/device-capabilities.md) information is sent from the device to the WFM using the [Device API](../../specification/margo-management-interface/device-capabilities.md)

## Onboarding Sequence diagram

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Server

    Note over Client,Server: 🔐 Initial Trust Establishment
    Note over Client,Server: The device's management client obtains the WFM's root CA certificate either out-of-band or via the Certificate API over an existing trusted channel.
    Client->>Server: GET /onboarding/certificate
    Server-->>Client: Base64-encoded Root CA certificate
    Client-->>Client: Injecting Root CA into trusted store

    Note over Client,Server: 🔒 Standard TLS Handshake Start
    Client->>Server: TLS ClientHello (TLS versions, cipher suites, random)
    Server-->>Client: TLS ServerHello (chosen version, cipher, random)
    Server-->>Client: X.509 certificate chain(server + intermediate(if applicable))
    Client-->>Client: Verifies server cert chain based on RootCA
    Note over Client,Server: 🔒 Standard TLS Handshake completed
    WFMUser->>Server: Opportunity for user to manually upload client certificate
    Note over Client,Server: Device Client onboarding begins
    Client->>Server: POST /onboarding using the device's public certificate (could exchange additional info)
    WFMUser->>Server: Opportunity for user to approve or reject client onboarding
    alt Public key trusted/user approved
        Note over Server: Server verifies client certificate and assigns UUID
        Server-->>Client: 201 Created {clientId}
    else Client rejected
        Server-->>Client: 400 Bad Request {error: "Invalid certificate"}
    else Client rejected
        Server-->>Client: 403 Forbidden {error: "Client rejected"}
    end

    Note over Client,Server: Device Client onboarding Ends
    Note over Client,Server: 📡 Secure API Usage with Signed Payloads can now begin

    Client->>Server: POST /clients/{clientId}/capabilities
    Server-->>Client: 201 Created
    Note over Client,Server: Enrollment is complete
    Note over Client,Server: 📡 Secure API Usage with Signed Payloads
    Client->>Server: POST /clients/{clientId}/deployments/{deploymentId}/status
    Server-->>Client: 201 Created
```

## Onboarding API Details

## Route and HTTP Methods

```https
POST /api/v1/onboarding
```
## Request Body Attributes

| Fields       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version the API resource follows.|
| kind            | string    | Y    | Must be `OnboardingRequest`.|
| certificate    | string    | Y    | Base64-encoded X.509 certificate of the client. |

### Example Request Body

```json
{ 
  "apiVersion": "onboarding.margo.org/v1alpha1",
  "kind": "OnboardingRequest",
  "certificate": "MIIDdzCCAl+gAwIBAgIEb1...<truncated Base64 X.509 cert>...."
}
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
    "clientId": "<base-64 encoded UUID or other URL safe string identifier>"
}
```


