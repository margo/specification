# Device Client Onboarding

To enable workload management, the device's client first establishes trust and completes an onboarding process with the End Users' selected Workload Fleet Manager. This onboarding process enables late binding, which is a critical Margo non-functional requirement that enables a device to bind to any Margo-compatible Workload Fleet Manager. 

The onboarding process includes several core functions:

- Establishing trust between the device and the WFM
- Registering the device client and assigning a unique identifier
- Reporting device capabilities to enable workload placement decisions

## Trust Establishment

Initial trust is established between the device's Workload Fleet Management (WFM) Client and the WFM using server-side TLS.
Before the WFM Client can connect securely, it obtains the WFM's root CA certificate. This trust anchor can be:

- downloaded via the Certificate API, provided that an existing trusted channel is available, or
- delivered out-of-band (e.g., preloaded by the device owner or transferred via USB)

Importing the WFM's root CA certificate enables the WFM Client to authenticate the WFM during TLS connections. Mutual TLS (mTLS) is deliberately avoided, as some deployment environments include network components or intermediaries that may not support or forward client-certificate authentication.
Instead, transport security and server authentication are provided by server-side TLS, while client authentication and request integrity are performed at the application layer: the WFM Client uses its own X.509 certificate to create HTTP message signatures for each request. This approach maintains strong, certificate-based authenticity and integrity while accommodating a wide range of network architectures.


## Certificates required

Both the WFM server and the WFM Client use X.509 certificates, but for different purposes. The WFM's certificate authenticates the server during TLS sessions. Each device client possesses a unique X.509 certificate used to sign its HTTP requests, enabling the WFM to verify the origin and integrity of every message. These certificates provide complementary security properties: TLS ensures transport confidentiality and server authenticity, while application-layer signatures provide client authentication and payload integrity. Private keys remain securely stored on the device, and all signing operations occur locally, reducing exposure to key compromise.


## Unique Identifiers

The Workload Fleet Manager assigns a globally unique identifier to the device's management client during the onboarding process. This is needed to ensure unique interactions between each device with the Fleet Manager. 

## Device Capability Reporting

After onboarding, the device client reports its capabilities to the WFM server using the device capability reporting API.

## Relevant Links

Please follow the subsequent links to view more technical information on the concepts described above:

- [API Security Details](../../specification/margo-management-interface/api-requirements-and-security.md)
- [Certificate API](../../specification/margo-management-interface/certificate-api.md)
- [Device Onboarding API](../../specification/margo-management-interface/device-client-onboarding.md)
- [Device Capabilities](../../specification/margo-management-interface/device-capabilities.md)