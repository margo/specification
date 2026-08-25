# Trust Bundle and Discovery

The MIS role serves two read-only HTTPS endpoints: an optional **discovery document** that points a client to the Trust Bundle, and the **Trust Bundle retrieval** endpoint itself. Because the MIS is a role rather than a fixed service (see [The MIS role](./identity-framework.md#the-mis-role)), the origin hosting these endpoints is chosen by the MIS implementation; this section constrains only the path convention (when discovery is used) and the response payloads.

Both endpoints MUST be served over HTTPS authenticated per [initial trust bootstrap](./tls-requirements.md#initial-trust-bootstrap), and a client MUST tolerate unknown response fields so that future revisions can add fields without breaking existing implementations.

A machine-readable description of both endpoints is available as the [Trust Bundle API OpenAPI definition](./trust-bundle-api-swagger.md).

## Discovery Document Endpoint

The discovery document is an optional entry point to a Trust Domain that points a client to the Trust Bundle URI. Each document describes exactly one Trust Domain.

When discovery is used, an origin serving exactly one Trust Domain SHOULD expose the document at `GET /.well-known/margo`; an origin serving several Trust Domains MAY use other absolute HTTPS URLs. When discovery is not used, the Trust Bundle URI is supplied by operator-provided configuration.

The endpoint requires no authentication at the application layer; the transport is authenticated per [initial trust bootstrap](./tls-requirements.md#initial-trust-bootstrap).

### Route and HTTP Methods

```https
GET /.well-known/margo
```

The path above is the default convention; an origin serving several Trust Domains MAY serve the document at another absolute HTTPS URL.

### Request Headers

| Header | Description |
| ------ | ----------- |
| `Accept` *(optional)* | The client SHOULD request the document in `application/json`. |
| `If-None-Match` *(optional)* | The `ETag` from the last successfully retrieved document, used to revalidate a cached copy. |

### Response Codes

| Code | Description |
| ---- | ----------- |
| 200 OK | The response body contains the discovery document. The server SHOULD include an `ETag` for cache revalidation. |
| 304 Not Modified | The cached copy is still valid; returned when the `If-None-Match` `ETag` matches. The response body is empty. |
| 404 Not Found | No discovery document is available at this origin. |

### Response Body Attributes

| Field | Type | Required? | Description |
| :---- | :--- | :-------- | :---------- |
| `trustDomain` | string | Y | Identifier of the Trust Domain (for example, `factory.example`). Every SPIFFE ID issued by the MIS MUST belong to this Trust Domain. |
| `trustBundleUri` | string | Y | Absolute HTTPS URL to the **SPIFFE bundle** for this Trust Domain, conforming to the [SPIFFE bundle format](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md#4-spiffe-bundle-format) and holding the domain's authoritative trust anchors. The resource SHOULD expose an `ETag` for cache revalidation. |

A client MUST ignore unknown fields in the discovery document.

A client that already holds an SVID SHOULD verify that the document's `trustDomain` matches the trust domain of its own SPIFFE ID and treat a mismatch as a configuration error; on an origin serving several Trust Domains, this check is what catches a client pointed at the wrong Trust Domain's document.

### Example Discovery Document Response

Request:

```http
GET /.well-known/margo
Accept: application/json
```

Response (`200 OK`):

```json
{
  "trustDomain": "factory.example",
  "trustBundleUri": "https://mis.factory.example/.well-known/spiffe/bundle.json"
}
```

## Trust Bundle Retrieval Endpoint

The resource identified by `trustBundleUri` returns the Trust Domain's SPIFFE bundle, which holds the authoritative set of public trust anchors for that Trust Domain. The endpoint follows the SPIFFE [bundle endpoint](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Federation.md) model, where one URL serves one Trust Domain's bundle.

The endpoint requires no authentication at the application layer; the transport is authenticated per [initial trust bootstrap](./tls-requirements.md#initial-trust-bootstrap). A client cannot yet validate MIAF-issued SVIDs when it first retrieves trust material, so this connection relies on an initial trust mechanism established outside MIAF, not on a MIAF SVID. When `trustBundleUri` names a different origin than the discovery document, the client's initial-trust material (configured PKI anchors or operator-provisioned pins) MUST cover that origin.

### Route and HTTP Methods

```https
GET <trustBundleUri>
```

`trustBundleUri` comes from the discovery document or from operator configuration and is an absolute HTTPS URL (for example, `https://mis.example.com/.well-known/spiffe/bundle.json`). A client MUST reject a `trustBundleUri` whose scheme is not `https`.

### Request Headers

| Header | Description |
| ------ | ----------- |
| `Accept` *(optional)* | The client SHOULD request the bundle in `application/json`. |
| `If-None-Match` *(optional)* | The `ETag` from the last retrieved bundle, used to revalidate a cached copy. |

### Response Codes

| Code | Description |
| ---- | ----------- |
| 200 OK | The response body is a SPIFFE bundle conforming to the [SPIFFE bundle format](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md#4-spiffe-bundle-format). The server SHOULD include an `ETag` for cache revalidation. |
| 304 Not Modified | The cached copy is still valid; returned when the `If-None-Match` `ETag` matches. The response body is empty. |
| 404 Not Found | The bundle is unavailable. |

### Example Bundle Response

The bundle carries the Trust Domain's X.509 trust anchors as JWK entries with `"use": "x509-svid"`. Each authority's certificate travels in `x5c` (base64-encoded DER). During a [trust anchor rotation](./identity-lifecycle.md#trust-anchor-rotation-playbook) overlap the `keys` array carries more than one `x509-svid` entry.

Response (`200 OK`):

```json
{
  "spiffe_sequence": 12,
  "spiffe_refresh_hint": 86400,
  "keys": [
    {
      "kty": "EC",
      "crv": "P-256",
      "x": "<base64url-encoded EC public key x coordinate>",
      "y": "<base64url-encoded EC public key y coordinate>",
      "use": "x509-svid",
      "x5c": ["<base64 DER of the Trust Domain's X.509 authority certificate>"]
    }
  ]
}
```

### Selecting and Refreshing the Bundle

A client uses the retrieved bundle as the authoritative source when validating SVIDs issued within the Trust Domain. A client that retrieves a bundle carrying no X.509 trust anchors MUST reject it and MUST NOT validate SVIDs against it, failing closed rather than proceeding with an empty anchor set.

A client MUST NOT validate SVIDs against a retrieved bundle it rejects (see the checks above). A client MUST keep validating SVIDs against its current bundle until it accepts a retrieved bundle. A failed or rejected retrieval therefore does not change the trust material the client uses. When a client accepts a retrieved bundle, the client MUST NOT combine trust anchors from its current bundle with trust anchors from the retrieved bundle. The trust anchors in the retrieved bundle replace all trust anchors the client used before. An anchor the operator removed from the published bundle to revoke a compromise would otherwise stay in use (see step 4 of the [trust anchor rotation playbook](./identity-lifecycle.md#trust-anchor-rotation-playbook)).

A client SHOULD refresh its cached bundle at the interval given by the bundle's `spiffe_refresh_hint`, when present, and otherwise at an operator-configured interval. This refresh cadence is authoritative: HTTP cache revalidation (`If-None-Match`/`304`, and any `Cache-Control` freshness) is an efficiency optimization within it and MUST NOT defer a refresh the interval requires. The refresh interval bounds how quickly a Trust Bundle rotation reaches the fleet; the [trust anchor rotation playbook](./identity-lifecycle.md#trust-anchor-rotation-playbook) depends on it. A client that cannot reach the bundle endpoint keeps using its cached bundle. MIAF sets no upper bound on bundle staleness (see [blocked Trust Bundle refresh](./identity-security-considerations.md#framework-threats)).

## Bundle Contents and Distribution

A Trust Bundle is distributed as a SPIFFE [bundle](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md), MAY additionally be delivered through deployment tooling or provisioning flows, and SHOULD be cached locally by a client to support offline validation.

The bundle contains the Trust Domain's X.509 trust anchors only; intermediate CA certificates travel with the presented SVID chain, not in the bundle (see [chain delivery](./svids.md#x509-svid-profile)).

A SPIFFE bundle is a JWK Set that MAY also carry JWT-SVID signing keys (`"use": "jwt-svid"`). MIAF uses only `x509-svid` entries; an implementation MUST ignore any `jwt-svid` or other non-`x509-svid` key material found in the bundle.
