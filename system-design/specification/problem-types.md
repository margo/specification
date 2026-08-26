# Problem Types

This catalogue defines the stable [RFC 9457](https://datatracker.ietf.org/doc/html/rfc9457) problem type identifiers reserved for the Margo specification namespace:

- https://docs.margo.org/specification/problem-types/

These values are used in the `type` field of RFC 9457 `application/problem+json` responses. They are intended to be stable identifiers for programmatic error handling, even when the actual HTTP responses are delivered through different API versions.

## Registry

| Type URI | HTTP status | Summary |
| --- | --- | --- |
| [#invalid-request](#invalid-request) | 400 | Malformed request body. |
| [#semantic-error](#semantic-error) | 422 | Request body includes a semantic error. |
| [#not-authorized](#not-authorized) | 403 | The request is not authorized by the WFM's local policy (for example, the client relationship has been retired). |
| [#gateway-not-found](#gateway-not-found) | 404 | No gateway was found for the given child-device deviceId. |
| [#device-not-found](#device-not-found) | 404 | No device with the given deviceId was found for the client. |
| [#invalid-bundle](#invalid-bundle) | 404 | Bundle not found for the given digest. |
| [#deployment-not-found](#deployment-not-found) | 404 | Deployment not found for the given digest. |
| [#discovery-document-not-found](#discovery-document-not-found) | 404 | Trust domain discovery document not available. |
| [#spiffe-bundle-not-found](#spiffe-bundle-not-found) | 404 | spiffe bundle unavailable. |
| [#server-cannot-generate-response](#server-cannot-generate-response) | 406 | Not Acceptable - Server cannot generate a response matching the Accept header. |

## Use in responses

A Margo API problem response MUST include a `type` value that matches one of the URIs in this catalogue whenever the condition is one of the standard Margo error categories. The canonical `type` value is the stable identifier; the HTTP status and `title` are descriptive metadata and are not a substitute for the URI.

---
## Registry Governance

### URI Stability and Versioning
Type URIs are **permanent stable identifiers and are intentionally unversioned**. The URI identifies the error *concept*, not the API version.

- `https://docs.margo.org/specification/problem-types#not-authorized` means "Not Authorized" in v1, v2, and all future versions — the concept does not change between API versions
- If an error concept changes significantly, a **new URI is added** and the old one **deprecated** — both remain valid during the transition period
- Existing URIs MUST NOT be repurposed or have their semantics changed
- Clients MUST treat each `type` URI as an opaque stable string

### Vendor Extensions
RFC 9457 §3.2 explicitly supports vendor-specific problem type URIs — there is no central registry. Suppliers MAY define additional problem types using their own URI namespace:

- Vendor URIs MUST use the supplier's own domain (e.g. `https://vendor.example.com/problems/sensor-fault`)
- Vendor URIs MUST NOT use the `https://docs.margo.org/specification/problem-types/` namespace, which is reserved for this specification
- Clients encountering an unknown `type` URI SHOULD fall back to using `title` and `detail` fields for display, and `status` for HTTP-level handling

### Deprecations

- Deprecated URIs are marked with `(deprecated)` in this registry
- Deprecated URIs remain valid for a minimum of two major specification versions
- A replacement URI MUST be listed alongside any deprecated URI

> **Note on URI Dereferenceability:** RFC 9457 §3.1.1 requires `type` to be a URI but does not require it to be dereferenceable at runtime. Clients MUST NOT fetch these URIs at runtime; they are stable identifiers only.

### `about:blank` Type URI

When no Margo-specific problem type applies, implementations MUST use `about:blank` as the `type` value. In this case the `title` SHOULD be the standard HTTP status phrase for the status code, and `detail` SHOULD describe the specific occurrence.

| `type` | HTTP Status | When to use |
| --- | --- | --- |
| `about:blank` | 404 | Not Found — resource does not exist and no specific Margo type applies |
| `about:blank` | 409 | Conflict — request conflicts with current state |
| `about:blank` | 429 | Too Many Requests — rate limit exceeded |
| `about:blank` | 500 | Internal Server Error — unexpected server error |
| `about:blank` | 501 | Not Implemented — feature not yet implemented |
| `about:blank` | 503 | Service Unavailable — server temporarily unable to handle request |

Example `about:blank` response for a rate limit:

```json
{
  "type": "about:blank",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit exceeded. Retry after the indicated period.",
  "instance": "/api/v1/deployments",
  "retryable": true,
  "backoffStrategy": "exponential"
}
```
---

## invalid-request

- **Type URI:** `https://docs.margo.org/specification/problem-types#invalid-request`
- **HTTP status:** 400 Bad Request
- **Summary:** Malformed request body.

This problem type indicates that the server rejected the request because the request body was malformed or could not be parsed.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#invalid-request",
  "title": "Invalid Request",
  "status": 400,
  "detail": "Malformed request body.",
  "instance": "/api/v1/capabilities/device-1"
}
```

---

## semantic-error

- **Type URI:** `https://docs.margo.org/specification/problem-types#semantic-error`
- **HTTP status:** 422 Unprocessable Entity
- **Summary:** Request body includes a semantic error.

This problem type is returned when the request body is syntactically valid but contains a semantic error. The `errors` array SHOULD be present with field-level details.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#semantic-error",
  "title": "Semantic Error",
  "status": 422,
  "detail": "Request body includes a semantic error.",
  "instance": "/api/v1/capabilities/device-1",
  "errors": [
    {
      "field": "properties.supportedRuntimes",
      "message": "must contain at least one valid runtime"
    }
  ]
}
```

---

## not-authorized

- **Type URI:** `https://docs.margo.org/specification/problem-types#not-authorized`
- **HTTP status:** 403 Forbidden
- **Summary:** The request is not authorized by the WFM's local policy.

This problem type identifies requests that are denied by the WFM's local authorization policy. This includes cases where the client relationship has been retired. Authentication via mTLS succeeded, but the WFM's policy does not permit this request.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#not-authorized",
  "title": "Not Authorized",
  "status": 403,
  "detail": "The request is not authorized by the WFM's local policy (for example, the client relationship has been retired).",
  "instance": "/api/v1/deployments"
}
```

---

## gateway-not-found

- **Type URI:** `https://docs.margo.org/specification/problem-types#gateway-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** No gateway was found for the given child-device deviceId.

This problem type indicates that the server cannot find a gateway for the child-device identified by the `deviceId` path parameter. This applies when a child `deviceId` is used and no parent gateway is registered for it.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#gateway-not-found",
  "title": "Gateway not found",
  "status": 404,
  "detail": "No gateway was found for the given child-device deviceId.",
  "instance": "/api/v1/capabilities/gateway-1/child-device-2"
}
```

---

## device-not-found

- **Type URI:** `https://docs.margo.org/specification/problem-types#device-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** No device with the given deviceId was found for the client.

This problem type is returned when a DELETE request references a device that does not exist for the authenticated client.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#device-not-found",
  "title": "Device Not Found",
  "status": 404,
  "detail": "No device with the given deviceId was found for the client.",
  "instance": "/api/v1/capabilities/device-1"
}
```

---

## invalid-bundle

- **Type URI:** `https://docs.margo.org/specification/problem-types#invalid-bundle`
- **HTTP status:** 404 Not Found
- **Summary:** Bundle not found for the given digest.

This problem type is returned when the referenced bundle archive cannot be served for the provided content-addressable digest.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#invalid-bundle",
  "title": "Invalid Bundle",
  "status": 404,
  "detail": "Bundle not found for the given digest.",
  "instance": "/api/v1/bundles/sha256:abc123"
}
```

---

## deployment-not-found

- **Type URI:** `https://docs.margo.org/specification/problem-types#deployment-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** Deployment not found for the given digest.

This problem type identifies requests for deployment content that cannot be retrieved for the requested deployment ID and content-addressable digest.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#deployment-not-found",
  "title": "Deployment Not Found",
  "status": 404,
  "detail": "Deployment not found for the given digest.",
  "instance": "/api/v1/deployments/app-42/sha256:abc123"
}
```

---

## server-cannot-generate-response

- **Type URI:** `https://docs.margo.org/specification/problem-types#server-cannot-generate-response`
- **HTTP status:** 406 Not Acceptable
- **Summary:** Not Acceptable - Server cannot generate a response matching the Accept header.

This problem type is used when the server cannot produce a response in the format or representation requested by the client's `Accept` header.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#server-cannot-generate-response",
  "title": "Server Cannot Generate Response",
  "status": 406,
  "detail": "Not Acceptable - Server cannot generate a response matching the Accept header.",
  "instance": "/api/v1/deployments"
}
```

---

## discovery-document-not-found

- **Type URI:** `https://docs.margo.org/specification/problem-types#discovery-document-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** Trust domain discovery document not available.

This problem type is returned when the Trust Domain discovery document is not available at the well-known path. This may occur when the Margo Identity Service (MIS) does not expose a discovery document, or when the document has not yet been provisioned. Clients SHOULD fall back to operator-provided Trust Bundle URI configuration when this error is encountered.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#discovery-document-not-found",
  "title": "Discovery Document Not Found",
  "status": 404,
  "detail": "Trust domain discovery document not available.",
  "instance": "/.well-known/margo"
}
```

---

## spiffe-bundle-not-found

- **Type URI:** `https://docs.margo.org/specification/problem-types#spiffe-bundle-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** SPIFFE bundle unavailable.

This problem type is returned when the SPIFFE Trust Bundle cannot be retrieved from the Margo Identity Service (MIS). Clients MUST NOT validate SVIDs when the Trust Bundle is unavailable and SHOULD retry using the backoff strategy indicated in the response.

```json
{
  "type": "https://docs.margo.org/specification/problem-types#spiffe-bundle-not-found",
  "title": "Bundle Not Found",
  "status": 404,
  "detail": "SPIFFE bundle unavailable.",
  "instance": "/.well-known/spiffe/bundle.json",
  "retryable": true,
  "retryAfterSeconds": 30,
  "backoffStrategy": "exponential"
}
```