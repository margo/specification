# WFM Identity Profile

The WFM Identity Profile is the first identity profile under the [Margo Identity and Authorization Framework](./identity-framework.md). It covers both the **WFM identity** and the **WFM Client identity**: how each is named, how each is recognized, how each is provisioned, and how the WFM authenticates and authorizes a caller at its API.

A WFM holds an identity within the Trust Domain that anchors its namespace. A WFM Client holds an identity within that same Trust Domain, named under the WFM that issues it. Authentication is mutual: a WFM Client presents its X.509-SVID and validates the WFM's SVID, and the caller identity at the WFM API is the authenticated WFM Client SPIFFE ID carried over mTLS.

All MIAF terminology is reused by reference from the [MIAF terminology](./identity-framework.md#terminology) unless specialized here. The two identities this profile introduces, the **WFM Identity** and the **WFM Client Identity**, are defined in the [Identity Model](#identity-model) below.

## Identity Model

### WFM Identity

A WFM identity is a SPIFFE ID of the form:

```text
spiffe://<trust-domain>/margo/wfm/<wfm-id>
```

The `wfm-id` segment:

- MUST be non-empty, MUST consist only of letters, digits, dots, dashes, and underscores, and MUST NOT be `.` or `..`, per [SPIFFE ID, Section 2.2](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md#22-path);
- MUST be unique within the Trust Domain;
- MUST be stable for the life of the WFM identity it names. Rebinding a `wfm-id` to a different WFM identity is not defined by this profile and MUST NOT be performed silently; replacement requires a new `wfm-id`; and
- SHOULD be assigned by the operator deploying the WFM into the Trust Domain, not unilaterally by the WFM vendor, so that operators can prevent namespace collisions in multi-vendor deployments.

An operator MAY assign one shared `wfm-id` across several WFM instances to present a single logical identity, or distinct `wfm-id`s for each instance for finer-grained lifecycle management.

The two options have different security costs. A WFM Client takes its expected `wfm-id` from its own SVID (see [Recognition by the WFM Client](#recognition-by-the-wfm-client)), so it can fail over only to instances that share that `wfm-id`. A shared `wfm-id` is therefore the usual choice for high availability. All instances then present one SPIFFE ID, so no verifier can tell them apart, and the operator cannot revoke one instance alone. Trust Bundle rotation or expiry are then the only ways to withdraw a compromised instance (see [no precise revocation of a compromised WFM](./identity-security-considerations.md#wfm-identity-profile-threats)). Where the instances share one private key, each instance holds a copy of the key that can leak (see the theft and key-custody rows of the [framework threats](./identity-security-considerations.md#framework-threats)). SPIFFE permits several key pairs under one SPIFFE ID. Whether an MIS issues them depends on the MIS, and a stock CA does not prevent it.

A WFM participating in this profile:

- MUST hold a valid WFM X.509-SVID; and
- MUST use the same `wfm-id` in its own SPIFFE ID and in the SPIFFE IDs of the WFM Clients it accepts.

The WFM is a principal under MIAF and obtains its SVID through one of the MIAF [acquisition modes](./credential-provisioning.md#acquisition-modes) (see [Provisioning](#provisioning)).

### WFM Client Identity

A WFM Client identity is a SPIFFE ID of the form:

```text
spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/<wfm-client-id>
```

The `wfm-client-id` segment:

- MUST be non-empty, MUST consist only of letters, digits, dots, dashes, and underscores, and MUST NOT be `.` or `..`, per [SPIFFE ID, Section 2.2](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md#22-path);
- MUST be unique within the issuing WFM's namespace; and
- MUST be stable for the lifetime of the relationship.

The `wfm-id` and `wfm-client-id` segments carry no meaning beyond naming the WFM and the client relationship: apart from the recognition checks defined in this profile, a WFM Client MUST NOT infer structure or attributes from their content. All comparisons of these segments are exact and case-sensitive, following SPIFFE path semantics. This SPIFFE ID is the canonical WFM Client identity within the Trust Domain.

### Identity Representation

X.509-SVID is the representation used for WFM and WFM Client authentication, per the MIAF [X.509-SVID profile](./svids.md#x509-svid-profile).

### Recognition by the WFM

A WFM MUST recognize a WFM Client from the authenticated SPIFFE ID alone. When a WFM Client connection is established, the WFM MUST:

1. validate the presented SVID against the Trust Domain's Trust Bundle;
2. extract the SPIFFE ID from the URI SAN and verify that it has the exact form `spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/<wfm-client-id>`, where `<trust-domain>` and `<wfm-id>` are those of the WFM's own identity; and
3. reject the connection if the SPIFFE ID does not have this form, or if its `<trust-domain>` or `<wfm-id>` does not match the WFM's own.

A WFM MUST NOT treat a peer as one of its clients when the peer's SPIFFE ID does not match this shape, even if that SVID is validly issued within the Trust Domain.

Over the life of the connection, the WFM SHOULD bound connection lifetime per the MIAF [session lifetime and re-validation](./tls-requirements.md#session-lifetime-and-re-validation) rules, and MUST authorize each request using local policy keyed on the WFM Client identity, per [Authorization](#authorization).

### Recognition by the WFM Client

A WFM Client MUST recognize the WFM it connects to from the authenticated SPIFFE ID alone. The WFM a client may talk to is fully determined by the client's own SVID: a client named `spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/<wfm-client-id>` belongs to the WFM `spiffe://<trust-domain>/margo/wfm/<wfm-id>` in the same Trust Domain. The client takes the expected `<trust-domain>` and `<wfm-id>` from its own SVID rather than from separate configuration. For each connection, the WFM Client MUST:

1. validate the presented WFM SVID against the Trust Domain's Trust Bundle;
2. extract the SPIFFE ID from the URI SAN;
3. verify that the SPIFFE ID is exactly `spiffe://<trust-domain>/margo/wfm/<wfm-id>`, using the `<trust-domain>` and `<wfm-id>` of the client's own SVID; and
4. abort the connection if any of these checks fails.

A WFM Client holding a long-lived connection SHOULD limit the connection's lifetime, or otherwise re-validate the WFM SVID, per the MIAF [session lifetime and re-validation](./tls-requirements.md#session-lifetime-and-re-validation) rules, rather than relying solely on the connection-time check above.

## Provisioning

WFM and WFM Client SVIDs are both acquired through the MIAF [acquisition modes](./credential-provisioning.md#acquisition-modes) and provisioned per the MIAF [provisioning input contract](./credential-provisioning.md#provisioning-input-contract). For the installed mode and for manual issuance in the enrolled mode, the operator follows the [operator provisioning playbook](./identity-lifecycle.md#operator-provisioning-playbook). This profile adds only what is specific to its two principal classes: the SPIFFE path each SVID carries, the inputs specific to each class, and the steps that establish the client relationship.

**For each WFM**, the operator chooses a `wfm-id` for the WFM namespace and issues the SVID with the URI SAN `spiffe://<trust-domain>/margo/wfm/<wfm-id>`.

**For each WFM Client**, the operator:

1. chooses a `wfm-id` for the target WFM (matching the WFM's `wfm-id`) and a `wfm-client-id` for this client relationship, and issues the SVID with the URI SAN `spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/<wfm-client-id>`;
2. configures the client with the WFM's endpoint URL. The client uses the URL only to connect: the client authenticates the WFM by its SVID, matching it against the `<trust-domain>` and `<wfm-id>` carried in the client's own SVID per [Recognition by the WFM Client](#recognition-by-the-wfm-client), not by the URL; and
3. adds the new `wfm-client-id` (or full SPIFFE ID) to the target WFM's accepted-client policy, so that the WFM will authorize requests from this client per [Authorization](#authorization).

### Provisioning Inputs

In addition to the [inputs for all principals](./credential-provisioning.md#inputs-and-output-for-all-principals), each principal class accepts the inputs below.

**WFM Client only:**

| Input | Required | Notes |
| :---- | :------- | :---- |
| WFM endpoint URL | always | the client uses it only to connect to the WFM. It does not authenticate the WFM by this URL (see step 2 above) |

A WFM Client needs no separate input for its target `wfm-id`. It reads the `wfm-id` from its own SVID, because this profile names the client under its target WFM. The WFM endpoint URL is therefore the only configuration a WFM Client needs beyond the inputs for all principals.

**WFM only:**

| Input | Required | Notes |
| :---- | :------- | :---- |
| Accepted-client policy entries | always | the WFM Client identities the WFM authorizes, per [Authorization](#authorization) |

A WFM MUST be configurable with the set of WFM Client identities it authorizes, as an explicit list of identifiers (`wfm-client-id` or full SPIFFE ID). The namespace option in [Authorization](#authorization) stays available alongside the list. List serialization is product-specific, and how an operator manages the set at runtime is out of scope.

## Lifecycle

The MIAF [lifecycle vocabulary](./identity-lifecycle.md#lifecycle-vocabulary) applies to both WFM and WFM Client identities. The **Active** phase has a fully normative protocol surface: a client authenticates to a WFM over mTLS using its X.509-SVID per the Management Interface [identity and authentication](../margo-management-interface/api-requirements-and-security.md#identity-and-authentication) rules, and validates the WFM SVID per [Recognition by the WFM Client](#recognition-by-the-wfm-client). The other phases are operator-driven:

| Phase | WFM | WFM Client |
| :---- | :--------- | :--------- |
| Enrollment | Issue and deliver an SVID with URI SAN `spiffe://<trust-domain>/margo/wfm/<wfm-id>` through the WFM's acquisition mode. | Issue and deliver an SVID with URI SAN `spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/<wfm-client-id>` through the client's acquisition mode; add `wfm-client-id` to the WFM's accepted-client policy. |
| Renewal | Issue a replacement SVID (same SPIFFE ID) before expiry, through the same acquisition mode. | Issue a replacement SVID (same SPIFFE ID) before expiry, through the same acquisition mode. |
| Revocation | Rotate the Trust Bundle to invalidate the issuing CA (this also invalidates the WFM Clients issued under that CA). See the MIAF [operator revocation playbook](./identity-lifecycle.md#operator-revocation-playbook). | Remove `wfm-client-id` from the WFM's accepted-client policy. For mass revocation, rotate the Trust Bundle. |
| Re-issuance | Issue a new SVID with the same SPIFFE ID to the replacement WFM. | Issue a new SVID (same or new `wfm-client-id`, per operator policy) to the replacement principal; update the WFM's accepted-client policy if the identifier changed. |

WFM revocation is heavier-handed than WFM Client revocation because there is no client-side accepted-server allowlist comparable to the WFM's accepted-client policy. An operator reissues the WFM SVID (keeping the same SPIFFE ID) in most cases; Trust Bundle rotation is the cryptographically enforced revocation path.

Removing a `wfm-client-id` withdraws one client only where the accepted-client policy lists clients individually. Where a WFM instead accepts any client within its namespace (see [Authorization](#authorization)), there is no individual entry to remove, so withdrawing a single client requires narrowing the policy to explicit entries or rotating the Trust Bundle.

### Rebinding a WFM Client (informative)

Moving a WFM Client to a different WFM requires a new Enrollment with a new SPIFFE ID. The reason is the naming scheme: a client's SPIFFE ID contains its target WFM (`.../wfm/<wfm-id>/client/<wfm-client-id>`), and an identity in a certificate cannot be edited. Binding the client to a different WFM therefore produces a new identity, and the move consists of four changes:

1. a new SVID, naming the client under the new WFM;
2. the new WFM endpoint URL;
3. an entry added to the accepted-client policy of the new WFM; and
4. the old entry removed from the policy of the previous WFM.

Every artifact in the move is a provisioning input: the SVID, the endpoint URL, and the accepted-client policy on each side (see [Provisioning inputs](#provisioning-inputs)). The move therefore needs no vendor-specific steps. The same artifacts and workflow rebind a client between any two conformant products.

### Identity Failure and Deployed Workloads

A WFM Client can lose the ability to authenticate: its SVID expires, it holds no usable Trust Bundle, or it cannot validate the WFM's SVID (for example, because its clock is wrong). The mTLS rules then stop its Management Interface calls, so the management plane fails closed. The WFM Client MUST NOT stop, remove, or change workloads already deployed because of such a failure. It SHOULD raise an operator-visible signal while the failure lasts.

In industrial deployments, availability often has priority over other security objectives (see also IEC 62443, FR 7, resource availability). After an identity failure, the last applied desired state therefore stays in effect, and the workloads keep running.

## Authorization

A WFM MUST authorize each request using local policy keyed on the authenticated WFM Client identity. Recognizing the SPIFFE ID (see [Recognition by the WFM](#recognition-by-the-wfm)) establishes only that the caller is a validly issued client within this WFM's namespace; it does not by itself grant access.

A WFM MUST maintain an accepted-client policy and admit a caller only when its identity is accepted by that policy; a matching `wfm-id` namespace is necessary but not sufficient. The policy MAY accept named `wfm-client-id`s (or full SPIFFE IDs) individually, and MAY accept any client within this WFM's namespace where the operator trusts the [MIS](./identity-framework.md#the-mis-role) to issue identities under `spiffe://<trust-domain>/margo/wfm/<wfm-id>/client/` only to authorized clients. An operator SHOULD constrain the MIS to issue SVIDs under a WFM's namespace only to that WFM's authorized clients. The policy is configurable as an explicit list, per [provisioning inputs](#provisioning-inputs). Beyond that, how the policy is expressed is implementation-specific; the requirement is that acceptance is an explicit local decision, not an automatic consequence of holding a valid SVID. Policy MAY further consider deployment-specific `wfm-client-id` metadata, and a WFM MAY deny a request from a still-valid credential; for example, once a client relationship has been retired.

How this profile applies to the Margo Management Interface is specified in [API Requirements and Security](../margo-management-interface/api-requirements-and-security.md#identity-and-authentication): the endpoints served, the mTLS authentication of each call, the handling of caller identity, and how an authorization denial is surfaced (HTTP status and response body).
