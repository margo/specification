# Device Client Onboarding

Within Margo, late binding is an important non-functional requirement that enables a device to bind to any Margo compatible Workload Fleet Manager. To enable workload management, the device's client must first establish trust and complete an onboarding procedure with the End Users selected Workload Fleet Manager.  

The onboarding process includes the following major functions within Margo:
- trust establishment
- client onboarding
- device capability reporting

## Trust Establishment

Initial trust is established between the device’s management client and the Workload Fleet Management (WFM) web service using server-side TLS. The device downloads the WFM’s public root CA certificate via the onboarding API, or receives it via out-of-band strategies. The device injects the root CA into its trusted store, enabling secure TLS handshakes and certificate validation. This process avoids mTLS due to infrastructure compatibility concerns and relies on certificate-based trust.

## Certificates required

Both the WFM server and device clients use X.509 certificates for identity and secure communication. The server’s certificate is used for TLS authentication; the device client is issued a unique certificate for payload signing and integrity. Certificates are used to sign API payloads, ensuring authenticity and integrity. Private keys are securely stored and used for signing operations.

## Unique Identifiers

The Workload Fleet Manager assigns a unique identifier to the device's management client during the onboarding process. This is needed to ensure unique interactions between each device with the Fleet Manager. Unique identifiers 

## Device Capability Reporting

After onboarding, the device client reports its capabilities to the WFM server using the Device API. The API operates over REST/HTTP1.1, exclusively on port 443.
Payloads are signed using the device’s X.509 certificate:
- The client creates a SHA256 hash of the base64-encoded payload (Content-Digest).
- A signature base string is constructed and signed with the client’s private key.
- The signature and digest are included in the HTTP headers.

The WFM server verifies the signature using the client’s public key before processing the payload.

## The following pages provide further details on the concepts described above:
- [API Security Details](../../specification/margo-management-interface/api-requirements-and-security.md)
- [Certificate API](../../specification/margo-management-interface/certificate-api.md)
- [Device Onboarding API](../../specification/margo-management-interface/device-onboarding.md)
- [Device Capabilities](../../specification/margo-management-interface/device-capabilities.md)