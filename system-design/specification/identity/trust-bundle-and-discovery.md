# Trust Bundle and Discovery

The MIS role serves two read-only HTTPS endpoints: an optional **discovery document** that points a client to the Trust Bundle, and the **Trust Bundle retrieval** endpoint itself. Because the MIS is a role rather than a fixed service (see [The MIS role](identity-framework.md#the-mis-role)), the origin hosting these endpoints is chosen by the MIS implementation; this section constrains only the path convention (when discovery is used) and the response payloads.

Both endpoints MUST be served over HTTPS authenticated per [initial trust bootstrap](tls-requirements.md#initial-trust-bootstrap), and a client MUST tolerate unknown response fields so that future revisions can add fields without breaking existing implementations.

A machine-readable description of both endpoints is available as the [Trust Bundle API OpenAPI definition](trust-bundle-api-swagger.md).

## Discovery Document Endpoint

The discovery document is an optional entry point to a Trust Domain that points a client to the Trust Bundle URI. Each document describes exactly one Trust Domain.

When discovery is used, an origin serving exactly one Trust Domain SHOULD expose the document at `GET /.well-known/margo` per [RFC 8615](https://datatracker.ietf.org/doc/html/rfc8615); an origin serving several Trust Domains MAY use other absolute HTTPS URLs. When discovery is not used, the Trust Domain identifier and Trust Bundle URI are supplied by operator-provided configuration.

The endpoint requires no authentication at the application layer; the transport is authenticated per [initial trust bootstrap](tls-requirements.md#initial-trust-bootstrap).

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
| `trustBundleUri` | string | Y | Absolute HTTPS URL to the **SPIFFE Bundle Map** resource for this Trust Domain. The resource MUST conform to the [SPIFFE Bundle Map specification](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md#5-spiffe-bundle-map) and MUST contain an entry for the domain named by `trustDomain`; that entry is the authoritative local Trust Bundle. The resource SHOULD expose an `ETag` for cache revalidation. |

A client MUST ignore unknown fields in the discovery document.

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

The resource identified by `trustBundleUri` returns a SPIFFE Bundle Map. The entry keyed by the local `trustDomain` holds the authoritative set of public trust anchors for that Trust Domain.

The endpoint requires no authentication at the application layer; the transport is authenticated per [initial trust bootstrap](tls-requirements.md#initial-trust-bootstrap). A client cannot yet validate MIAF-issued SVIDs when it first retrieves trust material, so this connection relies on an initial trust mechanism established outside MIAF, not on a MIAF SVID. When `trustBundleUri` names a different origin than the discovery document, the client's initial-trust material (configured PKI anchors or operator-provisioned pins) MUST cover that origin.

### Route and HTTP Methods

```https
GET <trustBundleUri>
```

`trustBundleUri` comes from the discovery document or from operator configuration and is an absolute HTTPS URL (for example, `https://mis.example.com/.well-known/spiffe/bundle.json`). A client MUST reject a `trustBundleUri` whose scheme is not `https`.

### Request Headers

| Header | Description |
| ------ | ----------- |
| `Accept` *(optional)* | The client SHOULD request the Bundle Map in `application/json`. |
| `If-None-Match` *(optional)* | The `ETag` from the last retrieved Bundle Map, used to revalidate a cached copy. |

### Response Codes

| Code | Description |
| ---- | ----------- |
| 200 OK | The response body is a SPIFFE Bundle Map conforming to the [SPIFFE Bundle Map format](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md#5-spiffe-bundle-map). The server SHOULD include an `ETag` for cache revalidation. |
| 304 Not Modified | The cached copy is still valid; returned when the `If-None-Match` `ETag` matches. The response body is empty. |
| 404 Not Found | The bundle is unavailable. |

### Example Bundle Map Response

The Bundle Map is keyed by Trust Domain under `trust_domains`; the entry for the local `trustDomain` carries that domain's X.509 trust anchors as JWK entries with `"use": "x509-svid"`. Each authority's certificate travels in `x5c` (base64-encoded DER). During a [trust anchor rotation](identity-lifecycle.md#trust-anchor-rotation-playbook) overlap the `keys` array carries more than one `x509-svid` entry.

Response (`200 OK`):

```json
{
  "trust_domains": {
    "factory.example": {
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
  }
}
```

### Selecting and Refreshing the Bundle

A client selects the Trust Bundle for `trustDomain` from the retrieved Bundle Map and uses it as the authoritative source when validating SVIDs issued within the Trust Domain. A client that finds no entry for its `trustDomain`, or finds an entry that carries no X.509 trust anchors, MUST reject the Bundle Map and MUST NOT validate SVIDs against it, failing closed rather than proceeding with an empty anchor set. To resist rollback, where the Bundle Map carries `spiffe_sequence` a client SHOULD track the highest value it has accepted for the local Trust Domain and SHOULD reject a retrieved Bundle Map whose `spiffe_sequence` has regressed, since a lower value signals a stale, cached, or replayed bundle that could re-admit a trust anchor that was retired to revoke a compromise.

A client SHOULD refresh its cached bundle at the interval given by the bundle's `spiffe_refresh_hint`, when present, and otherwise at an operator-configured interval. This refresh cadence is authoritative: HTTP cache revalidation (`If-None-Match`/`304`, and any `Cache-Control` freshness) is an efficiency optimization within it and MUST NOT defer a refresh the interval requires. The refresh interval bounds how quickly a Trust Bundle rotation reaches the fleet; the [trust anchor rotation playbook](identity-lifecycle.md#trust-anchor-rotation-playbook) depends on it.

## Bundle Map Contents and Distribution

A Trust Bundle is distributed via the SPIFFE [Trust Domain and Bundle Map](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md), MAY additionally be delivered through deployment tooling or provisioning flows, and SHOULD be cached locally by a client to support offline validation.

A Trust Domain's bundle entry contains that domain's X.509 trust anchors only; intermediate CA certificates travel with the presented SVID chain, not in the bundle (see [chain delivery](svids.md#x509-svid-profile)).

The SPIFFE Bundle Map format reserves a slot for JWKS material. MIAF does not populate it, and an implementation MUST ignore any JWKS material found on retrieval.

A Bundle Map can carry the bundles of several Trust Domains, but from a given `trustBundleUri` only the entry keyed by that resource's local `trustDomain` is authoritative: a client MUST use that entry, and only that entry, as the trust anchors for the local Trust Domain. A client MUST NOT treat an entry for some other Trust Domain that happens to appear in the same map as authoritative for that domain; the trust anchors for another Trust Domain MUST be obtained from that domain's own authoritative source (its `trustBundleUri` or operator configuration), so that the operator of one domain's MIS cannot vouch for another domain. Where an operator configures cross-domain trust, packing the additional domain's bundle into one map MAY serve as a delivery convenience, but each domain's anchors remain bound to that domain's authoritative source. Full [SPIFFE Federation](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Federation.md) lifecycle semantics are out of scope.
