# Device Client Onboarding

To enable workload management, the device's client must first establish trust and complete an onboarding process with the End Users selected Workload Fleet Manager. This onboarding process enables late binding, which is a critical Margo non-functional requirement that enables a device to bind to any Margo compatible Workload Fleet Manager. 

The onboarding process includes several core functions:

- Establishing trust between the device and the WFM
- Registering the device client and assigning a unique identifier
- Reporting device capabilities to enable workload placement decisions

## Trust Establishment

Initial trust is established between the device’s management client and the Workload Fleet Management (WFM) web service using server-side TLS. The device downloads the WFM’s public root CA certificate via the onboarding API, or receives it via out-of-band strategies and injects into it's trusted certificate store. This enables secure TLS handshakes and certificate validation without requiring mutual TLS (mTLS), which was deliberately avoided due to infrastructure compatibility constraints. Instead, Margo relies on certificate-based trust, balancing security with operational simplicity.

## Certificates required

Both the WFM server and device clients use X.509 certificates for identity and secure communication. The WFM's certificate authenticates the server during TLS sessions, while each device's client is issued a unique certificate for signing payloads. These certificates ensure that every interaction is verifiable and tamper-proof. Private keys remain securely stored on the device, and all signing operations occur locally, reducing exposure to key compromise.

## Unique Identifiers

The Workload Fleet Manager assigns a globally unique identifier to the device's management client during the onboarding process. This is needed to ensure unique interactions between each device with the Fleet Manager. 

## Device Capability Reporting

After onboarding, the device client reports its capabilities to the WFM server using the device capability reporting API.


## The following pages provide further specification details on the concepts described above:
- [API Security Details](../../specification/margo-management-interface/api-requirements-and-security.md)
- [Certificate API](../../specification/margo-management-interface/certificate-api.md)
- [Device Onboarding API](../../specification/margo-management-interface/device-onboarding.md)
- [Device Capabilities](../../specification/margo-management-interface/device-capabilities.md)