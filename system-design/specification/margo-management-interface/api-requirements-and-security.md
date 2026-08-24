# API Requirements and Security Details
## General Requirements
- The Workload Fleet Management supplier MUST implement the server side of the API specification contract.
- The Device supplier, via it's WFM Client, MUST implement the client side of the API specification contract.

Below is a breakdown of the three major categories these requirements fall under:

1. Basic functions for supporting the Management Interface
    - Onboarding of the management interface client
2. Workload management functions
    - Set Desired State(s) assigned to particular device clients
3. Device client specific functions
    - Client Onboarding
    - Device Capability Reporting
    - Workload Status deployment reporting

### API Technical Overview
#### REST API Definition
The REST API is defined via the Open API Specification. 

- Follow the link below to see the specification:
    - [OpenAPI Specification](https://github.com/margo/specification/blob/pre-draft/system-design/specification/margo-management-interface/workload-management-api-1.0.0-rc.2.yaml)
    - [Swagger UI](../margo-management-interface/management-interface-swagger.md)
#### General Rest API information
Server-side TLS REST API MUST be utilized operating over HTTP1.1.

- The motivation to utilize HTTP1.1 is to ensure maximum support for existing infrastructure within our install base. 
- Server-side tls is utilized instead of mTLS due to possible issues with TLS terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection. See [Security and Integrity](#security-and-integrity-information) section for more details.
- The client MUST trust the WFM's server certificate through a pre-provisioned or securely obtained root CA.
    - The Certificate API MAY be used to retrieve this CA over an already trusted channel.

#### Authentication Mechanism
Initial trust is accomplished via TLS version 1.3 or greater

- The device establishes a secure HTTPS connection using server-side TLS.
- It validates the server’s identity using the public root CA certificate.
- Client authentication is achieved using application-layer HTTP Message Signatures (RFC 9421), as defined in the [Payload Security](#payload-security-method) section.

#### API Port Details

This API is designed to minimize the ports required on the customer's infrastructure to enable cloud to edge communication. 
    - The API MUST ONLY utilize port 443 for its traffic. 

#### Unique Identifiers

The WFM MUST create a URL-safe client ID to uniquely identify each client within the architecture. 

- This client ID MAY be in the format of UUIDv4
- Other URL safe string identifiers are permitted to be used


#### Certificate Information
Both the WFM and Device client MUST utilize X.509 certificates to represent themselves within the API interactions.

- The WFM's certificate is used to authenticate the server during TLS. The WFM Client’s certificate is used to authenticate the client and sign request payloads at the application layer, not during the TLS handshake. 
- All client certificates MUST conform to RFC 5280 standards. 
- Signature algorithm requirements:
    - Implementations MUST support the following set of allowable signature algorithms:
        - ecdsa-p256-sha256
        - ecdsa-p384-sha384
        - rsa-v1_5-sha256
        - rsa-pss-sha256
    - Additional algorithms MAY be supported, but the above list defines the minimum baseline for interoperability.
    - The server MUST support all required algorithms (see above), so it can verify any compliant client, while clients MAY choose any of the required algorithms that fits their hardware capabilities.


#### Support for Extended Device Communications Downtime
Interface patterns MUST support extended device communication downtime. 

- The Management Interface MUST allow an end user to configure the following:
	- Downtime configuration - ensures the device's management client is not retrying communication when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period. 
	- Polling Interval Period - describes a configurable time period indicating the hours in which the device's management client checks for updates to the device's desired state.
	- Polling Interval Rate - describes the rate for how frequently the device's management client checks for updates to the device's desire state.
- Running the device's management client as containerized services is preferred. By following Margo application packaging guidelines, it makes the management interface easier to lifecycle manage, however this is not required.

### Payload Security Method
#### Security and Integrity Information
Due to the limitations of utilizing mTLS with common OT infrastructure components, such as TLS-terminating HTTPS load-balancer or a HTTPS proxy doing lawful inspection, Margo has adopted a certificate-based payload signing approach to protect payloads from being tampered with. By utilizing the certificates to create payload envelopes (HTTP Request body), the device's management client can ensure secure transport between the device's management client and the Workload Fleet Management's web service.

- For API security, server-side TLS 1.3 (minimum) is used, where the keys are obtained from the Server's X.509 Certificate as defined in standard HTTP over TLS
- For API integrity, the device's management client is issued a client-specific X.509 certificate.
- The issuer of the client X.509 certificate is trusted under the assumption that the root CA download to the Workload Fleet Management server occurs as a precondition to onboarding the devices 
- Similarly, the issuer of the server X.509 certificate is  trusted under the assumption that the root CA download to the device's management client occurs over a "protected" connection as part of the yet to be defined device onboarding procedure
#### Device Management Client
Once the device management client has a message prepared for the Workload Fleet Management's web service, it MUST establish message integrity as defined in RFC 9421 by performing the following steps:

- The device's management client MUST generate a SHA256 digest of the HTTP request body. Encode the digest in Base64 and include it in the Content-Digest header. 
```
    Content-Digest: sha-256=:<base64(SHA256(body))>:
```
- The device management client MUST create a Signature Base String including @method, @target-uri, and Content-Digest. An example is given below.
```
    @method: POST
    @target-uri: https://api.example.com/resource
    Content-Digest: sha-256=:<digest>:
    @signature-params: ("@method" "@target-uri" "Content-Digest");created=1680575171;keyid="my-rsa-key"
```
- The device management client MUST generate the Signature field by signing the raw byte array of the Signature Base String using the clients X.509 private key. The resulting signature in Base64 is included in the Signature header. 
- The devices's management client MUST insert the following in the HTTP1.1 Header:
    - Content-Digest as formed above
    - Signature-Input as given below, replacing the created and keyid parts appropriately:
    ```
        sig1=("@method" "@target-uri" "Content-Digest");created=<Put created timestamp here>;keyid="<put the Key-Name here>"
    ```
    - Signature:
    ```
        sig1=:<base64(signature)>:
    ```

> Note: The server MUST use the `created` timestamp from the signature input to detect and prevent replay attacks. Requests with a `created` timestamp older than a configurable validity window (e.g., 5 minutes) or in the future (allowing for clock skew) MUST be rejected.

#### Workload Fleet Manager Web-Service           
- On receiving the message from the Device Client, the Workload Fleet Management's web service MUST do the following :
    - It looks up the client certificate from the Client-ID in the API Request URL 
    - The Workload Fleet Management's web service reads the following from the HTTP Request Header:
        - Signature-Input
        - Signature
        - Content-Digest (if body is present)
    - Use the Signature-Input in the header to determine which components were signed. Reconstruct the Signature Base canonical string using the actual values from the request, including the SHA256 encoded content-digest from the received request body 
    - Then extract the base64-encoded message signature from the Signature header and verifies the message signature string using the client's X.509 public-key.
    - If the message signature in the HTTP Header and the verified message signature match, then the payload is processed by the Workload Fleet Management's web service.
    - If the two do not match, the Workload Fleet Manager will respond with HTTP Error 401 as given below, and discontinue the session
      ```
      HTTP/1.1 401 Unauthorized
        Content-Type: application/json
        {
          "error": "Invalid signature",
          "message": "The X-Body-Signature header does not match the content of the request body."
        }
      ```
#### Open Source examples:
- Full RFC 9421 implementation with support for RSA, ECDSA, HMAC
     - [LINK](https://github.com/lestrrat-go/htmsig)
- Feature-complete RFC 9421 implementation with RSA-PSS and RSA-v1_5 support
     - [LINK](https://github.com/yaronf/httpsign)
