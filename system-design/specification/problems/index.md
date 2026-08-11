# Margo Problem Type Catalog

This catalogue defines the stable RFC 9457 problem type identifiers reserved for the Margo specification namespace:

- https://docs.margo.org/specification/problems/

These values are used in the `type` field of RFC 9457 `application/problem+json` responses. They are intended to be stable identifiers for programmatic error handling, even when the actual HTTP responses are delivered through different API versions.

## Registry

| Type URI | HTTP status | Summary |
| --- | --- | --- |
| [https://docs.margo.org/specification/problems/invalid-certificate-format](invalid-certificate-format.md) | 400 | Invalid certificate format or structure. |
| [https://docs.margo.org/specification/problems/invalid-digest-header](invalid-digest-header.md) | 400 | Missing or invalid content-digest header. |
| [https://docs.margo.org/specification/problems/invalid-request](invalid-request.md) | 400 | Invalid request. |
| [https://docs.margo.org/specification/problems/signature-verification-failed](signature-verification-failed.md) | 401 | Signature verification failed. |
| [https://docs.margo.org/specification/problems/semantic-error](semantic-error.md) | 422 | Request body includes a semantic error. |
| [https://docs.margo.org/specification/problems/certificate-not-trusted](certificate-not-trusted.md) | 403 | Client certificate is not trusted or has been revoked. |
| [https://docs.margo.org/specification/problems/invalid-client](invalid-client.md) | 404 | No client with the given client ID was found. |
| [https://docs.margo.org/specification/problems/invalid-bundle](invalid-bundle.md) | 404 | Bundle not found for the given digest. |
| [https://docs.margo.org/specification/problems/deployment-not-found](deployment-not-found.md) | 404 | Deployment not found for the given digest. |
| [https://docs.margo.org/specification/problems/server-cannot-generate-response](server-cannot-generate-response.md) | 406 | Server cannot generate a response matching the Accept header. |

## Use in responses

A Margo API problem response SHOULD include a `type` value that matches one of the URIs in this catalogue whenever the condition is one of the standard Margo error categories. The canonical `type` value is the stable identifier; the HTTP status and `title` are descriptive metadata and are not a substitute for the URI.

## Related specification text

The stable URI registry is defined as part of the RFC 9457 error response pattern and is intended to support interoperable programmatic handling across Margo releases.
