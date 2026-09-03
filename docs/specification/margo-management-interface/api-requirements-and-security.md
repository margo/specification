# API Requirements and Security Details
## General Requirements
- The Workload Fleet Management supplier MUST implement the server side of the API specification contract.
- The Device supplier, via its WFM Client, MUST implement the client side of the API specification contract.

Below is a breakdown of the two major categories these requirements fall under:

1. Workload management functions
    - Set Desired State(s) assigned to particular device clients
2. Device client specific functions
    - Device Capability Reporting
    - Workload Status deployment reporting
	
Identity and authentication for the Management Interface are provided by the [Margo Identity and Authorization Framework](../identity/identity-framework.md) and the [WFM Identity Profile](../identity/wfm-identity-profile.md). A WFM Client and a WFM are each provisioned with an X.509-SVID before any Management Interface call is made.


## API Definition
The REST API is defined via the OpenAPI Specification:

- [OpenAPI Specification](https://github.com/margo/specification/blob/pre-draft/system-design/specification/margo-management-interface/workload-management-api-1.0.0-rc.2.yaml)
- [Swagger UI](../margo-management-interface/management-interface-swagger.md)

## Transport
The REST API MUST operate over HTTP/1.1; HTTP/1.1 is used to ensure maximum support for existing infrastructure within our install base. The transport is secured by mTLS as specified in [Identity and Authentication](#identity-and-authentication).

To minimize the ports required on the customer's infrastructure for cloud-to-edge communication, the API MUST use port 443 for its traffic.

## Identity and Authentication
Authentication is mutual TLS per the MIAF [TLS requirements](../identity/tls-requirements.md). Both sides present an X.509-SVID and validate the peer's SVID and `wfm-id` per the WFM Identity Profile ([Recognition by the WFM](../identity/wfm-identity-profile.md#recognition-by-the-wfm), [Recognition by the WFM Client](../identity/wfm-identity-profile.md#recognition-by-the-wfm-client)). A WFM MUST reject any Management Interface request that is not authenticated by mTLS with a valid WFM Client X.509-SVID.

The caller identity for every request is the authenticated WFM Client SPIFFE ID; the request itself does not carry it. A WFM derives the caller from the SPIFFE ID, not from any identifier in the request path or body.

Every Management Interface endpoint is scoped to the authenticated caller. A WFM determines from the caller's identity which devices that client is responsible for and which deployments are assigned to them. Where a request path carries a resource identifier, for example `{deviceId}` or `{digest}`, the WFM looks that identifier up only among the resources in the caller's scope. A WFM MUST NOT expose or mutate a resource outside the caller's scope.

A `deviceId` is not a global name: it identifies a device only within the scope of one WFM Client. The binding between a `deviceId` and the caller's identity is established by the client itself, when it first reports capabilities for that device (see [Device Capabilities](../margo-management-interface/device-capabilities.md)), and every later reference to that `deviceId` is resolved within the reporting client's scope. Because the scope is derived from the authenticated SPIFFE ID, a client cannot register, read, or mutate a device in another client's scope: two clients reporting the same `deviceId` string address two unrelated device records. A WFM MAY additionally constrain, by local policy, which `deviceId`s a given client is allowed to report; such policy is deployment-specific and out of scope for this specification.

The WFM authorizes each request using local policy keyed on the authenticated WFM Client identity, and MAY deny a request from a still-valid credential, per [Authorization](../identity/wfm-identity-profile.md#authorization). When a WFM denies a request by local policy (for example, a retired client relationship), it SHOULD respond `403 Forbidden` with an [RFC 9457](https://datatracker.ietf.org/doc/html/rfc9457) Problem Details body (`Content-Type: application/problem+json`) using the `wfm-client-relationship-retired` type:

```json
{
  "type": "https://docs.margo.org/specification/problem-types#not-authorized",
  "title": "Client Relationship Retired",
  "status": 403,
  "detail": "The WFM Client relationship has been retired by local policy."											 
}
```

Both parties represent themselves with an X.509-SVID, an X.509 certificate carrying a SPIFFE ID in its URI SAN. SVID structure, key and signature algorithms, and validation follow the MIAF [X.509-SVID profile](../identity/svids.md#x509-svid-profile) and [cryptographic requirements](../identity/svids.md#cryptographic-requirements).

The Management Interface follows the MIAF [traffic-inspecting proxies](../identity/tls-requirements.md#traffic-inspecting-proxies) rules: a TLS-offloading proxy that forwards the validated client identity to the backend is supported, and an operator MUST exempt Margo mTLS endpoints from inline traffic inspection.

 

## Error Responses
All API error responses conform to [RFC 9457 Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc9457). Error responses are returned with `Content-Type: application/problem+json` and include a stable `type` URI that clients MUST use for programmatic error handling.

The standard error response structure is:
```json
{
  "type": "https://docs.margo.org/specification/problem-types#invalid-request",
  "title": "Invalid Request",
  "status": 400,
  "detail": "Malformed request body.",
  "instance": "/api/v1/capabilities/device-1"
}
```

| Field | Required | RFC 9457 Description |
| --- | --- | --- |
| `type` | No | Optional. If omitted, it defaults implicitly to about:blank. A URI reference identifying the problem type. Clients SHOULD use type as the primary identifier for programmatic error handling. |
| `title` | No | Optional. A short, human-readable summary of the problem type. For about:blank, the title is the same as the recommended HTTP status phrase for the status code. |
| `status` | No | Optional. It conveys the HTTP status code in the response body for convenience and consistency and SHOULD match the actual HTTP status code of the response. |
| `detail` | No | Optional. Human-readable explanation specific to this occurrence. |
| `instance` | No | Optional. URI reference identifying the specific occurrence of the problem. |
| `retryable` | No | Extension field. Whether the client MAY retry the request. |
| `backoffStrategy` | No | Extension field. Recommended retry strategy: `none`, `fixed`, or `exponential`. |
| `errors` | No | Extension field. Field-level validation errors. Common industry practice for validation failures (often 400 or 422). |

The full catalogue of registered Margo problem type URIs are defined in [Problem Types](../problem-types.md).

## Retry Semantics
Transient failures MUST communicate retry information as follows:

| Response | `Retry-After` Header | `retryable` | `backoffStrategy` |
| --- | --- | --- | --- |
| `429 Too Many Requests` | REQUIRED | `true` | `exponential` |
| `503 Service Unavailable` | REQUIRED | `true` | `exponential` |
| `500 Internal Server Error` | RECOMMENDED | `true` | `exponential` |
| All other errors | NOT applicable | `false` | `none` |

Clients MUST:
- Respect the `Retry-After` header value and MUST NOT retry before it elapses
- Use the `retryable` field to determine if retry is appropriate
- Apply `backoffStrategy` when retrying


## Extended Device Downtime
Interface patterns MUST support extended device communication downtime.

- The Management Interface MUST allow an end user to configure the following:
	- Downtime configuration - ensures the device's management client is not retrying communication when operating under a known downtime. Additionally, communication errors MUST be ignored during this configurable period.
	- Polling Interval Period - describes a configurable time period indicating the hours in which the device's management client checks for updates to the device's desired state.
	- Polling Interval Rate - describes the rate for how frequently the device's management client checks for updates to the device's desire state.
- Running the device's management client as containerized services is preferred. By following Margo application packaging guidelines, it makes the management interface easier to lifecycle manage, however this is not required.
