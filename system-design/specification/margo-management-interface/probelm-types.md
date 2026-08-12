# Problem Types

This catalogue defines the stable [RFC 9457](https://datatracker.ietf.org/doc/html/rfc9457) problem type identifiers reserved for the Margo specification namespace:

- https://docs.margo.org/specification/margo-management-interface/problem-types/

These values are used in the `type` field of RFC 9457 `application/problem+json` responses. They are intended to be stable identifiers for programmatic error handling, even when the actual HTTP responses are delivered through different API versions.

## Registry

| Type URI | HTTP status | Summary |
| --- | --- | --- |
| [#invalid-request](#invalid-request) | 400 | Malformed request body. |
| [#semantic-error](#semantic-error) | 422 | Request body includes a semantic error. |
| [#not-authorized](#not-authorized) | 403 | The request is not authorized by the WFM's local policy. |
| [#invalid-client](#invalid-client) | 404 | No gateway was found for the given child-device deviceId. |
| [#device-not-found](#device-not-found) | 404 | No device with the given deviceId was found for the client. |
| [#invalid-bundle](#invalid-bundle) | 404 | Bundle not found for the given digest. |
| [#deployment-not-found](#deployment-not-found) | 404 | Deployment not found for the given digest. |
| [#server-cannot-generate-response](#server-cannot-generate-response) | 406 | Not Acceptable - Server cannot generate a response matching the Accept header. |

## Use in responses

A Margo API problem response SHOULD include a `type` value that matches one of the URIs in this catalogue whenever the condition is one of the standard Margo error categories. The canonical `type` value is the stable identifier; the HTTP status and `title` are descriptive metadata and are not a substitute for the URI.

---

## invalid-request

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-request`
- **HTTP status:** 400 Bad Request
- **Summary:** Malformed request body.

This problem type indicates that the server rejected the request because the request body was malformed or could not be parsed.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-request",
  "title": "Invalid Request",
  "status": 400,
  "detail": "Malformed request body.",
  "instance": "/api/v1/capabilities/device-1"
}
```

---

## semantic-error

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/semantic-error`
- **HTTP status:** 422 Unprocessable Entity
- **Summary:** Request body includes a semantic error.

This problem type is returned when the request body is syntactically valid but contains a semantic error. The `errors` array SHOULD be present with field-level details.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/semantic-error",
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

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/not-authorized`
- **HTTP status:** 403 Forbidden
- **Summary:** The request is not authorized by the WFM's local policy.

This problem type identifies requests that are denied by the WFM's local authorization policy. This includes cases where the client relationship has been retired. Authentication via mTLS succeeded, but the WFM's policy does not permit this request.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/not-authorized",
  "title": "Not Authorized",
  "status": 403,
  "detail": "The request is not authorized by the WFM's local policy (for example, the client relationship has been retired).",
  "instance": "/api/v1/deployments"
}
```

---

## invalid-client

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-client`
- **HTTP status:** 404 Not Found
- **Summary:** No gateway was found for the given child-device deviceId.

This problem type indicates that the server cannot find a gateway for the child-device identified by the `deviceId` path parameter. This applies when a child `deviceId` is used and no parent gateway is registered for it.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-client",
  "title": "Invalid Client",
  "status": 404,
  "detail": "No gateway was found for the given child-device deviceId.",
  "instance": "/api/v1/capabilities/gateway-1/child-device-2"
}
```

---

## device-not-found

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/device-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** No device with the given deviceId was found for the client.

This problem type is returned when a DELETE request references a device that does not exist for the authenticated client.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/device-not-found",
  "title": "Device Not Found",
  "status": 404,
  "detail": "No device with the given deviceId was found for the client.",
  "instance": "/api/v1/capabilities/device-1"
}
```

---

## invalid-bundle

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-bundle`
- **HTTP status:** 404 Not Found
- **Summary:** Bundle not found for the given digest.

This problem type is returned when the referenced bundle archive cannot be served for the provided content-addressable digest.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/invalid-bundle",
  "title": "Invalid Bundle",
  "status": 404,
  "detail": "Bundle not found for the given digest.",
  "instance": "/api/v1/bundles/sha256:abc123"
}
```

---

## deployment-not-found

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/deployment-not-found`
- **HTTP status:** 404 Not Found
- **Summary:** Deployment not found for the given digest.

This problem type identifies requests for deployment content that cannot be retrieved for the requested deployment ID and content-addressable digest.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/deployment-not-found",
  "title": "Deployment Not Found",
  "status": 404,
  "detail": "Deployment not found for the given digest.",
  "instance": "/api/v1/deployments/app-42/sha256:abc123"
}
```

---

## server-cannot-generate-response

- **Type URI:** `https://docs.margo.org/specification/margo-management-interface/problem-types/server-cannot-generate-response`
- **HTTP status:** 406 Not Acceptable
- **Summary:** Not Acceptable - Server cannot generate a response matching the Accept header.

This problem type is used when the server cannot produce a response in the format or representation requested by the client's `Accept` header.

```json
{
  "type": "https://docs.margo.org/specification/margo-management-interface/problem-types/server-cannot-generate-response",
  "title": "Server Cannot Generate Response",
  "status": 406,
  "detail": "Not Acceptable - Server cannot generate a response matching the Accept header.",
  "instance": "/api/v1/deployments"
}
```
