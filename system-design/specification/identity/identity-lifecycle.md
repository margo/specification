# Identity Lifecycle and Operator Playbooks

## Lifecycle Vocabulary

A MIAF identity moves through five lifecycle phases:

1. **Enrollment**: initial issuance of an SVID for a principal.
2. **Active**: the principal holds a valid SVID and authenticates over mTLS, presenting its own SVID and validating each peer's SVID against the Trust Bundle, and is recognized by verifiers.
3. **Renewal**: refresh of an SVID before expiry.
4. **Revocation**: declaration that an issued SVID is no longer valid before its natural expiry.
5. **Re-issuance**: issuance of an SVID to a replacement principal (for example, after device replacement), typically reusing the original SPIFFE ID, though an operator MAY assign a fresh one.

The **Active** phase has a fully normative protocol surface. The other phases are operator-driven and follow the playbooks below.

> **Future work (informative)**
>
> Automated mechanisms for the non-active phases (enrollment, renewal, revocation, and re-issuance protocols) are not yet specified. Operator provisioning as described here is the current path and remains valid once automation is added.

## Operator Provisioning Playbook

The Trust Bundle and discovery document are the only runtime endpoints MIAF defines; everything else flows through the operator's existing provisioning channel.

For **enrollment**, the operator:

1. accepts a CSR from the principal (the preferred path, since it keeps the private key on the principal and supports hardware-bound keys such as a TPM, secure element, or HSM). Where the principal cannot generate its own key pair, the operator generates one centrally and accepts the resulting concentration of key custody;
2. mints an X.509-SVID for the chosen SPIFFE ID under the Trust Domain's issuing authority. The issuance is authoritative for the SPIFFE ID: any subject or SAN content the CSR carries is advisory and is overridden;
3. installs the SVID on the principal over a channel that protects its integrity and authenticity, and that additionally protects confidentiality on the path where it also carries the centrally generated private key; and
4. ensures every verifier the principal will authenticate to has the Trust Bundle and any local-policy entries needed to recognize the new SPIFFE ID.

For **renewal**, the operator repeats steps 1-3 before the current SVID expires, replacing the prior SVID in place.

For **re-issuance** after a principal is replaced, the operator follows the same workflow on the replacement principal. Reusing the original SPIFFE ID keeps the retired principal's SVID valid under the same identity until it expires, and no allowlist removal can withdraw the old credential without also withdrawing the replacement's access. An operator SHOULD assign a fresh SPIFFE ID unless the retired principal's private key is known to be destroyed, or its SVID is close enough to expiry that the operator accepts the overlap.

The provisioning channel itself is deployment-specific and out of scope. Typical options include device-management tooling, configuration management, HSM workflows, and out-of-band installer media.

## Operator Revocation Playbook

Without an automated revocation protocol, a deployment withdraws an SVID's access through one of:

1. **Verifier allowlist removal**: where a verifier keeps an allowlist of the identities it accepts, the operator removes the SPIFFE ID from it. This withdraws authorization at the application layer - the certificate itself is not revoked and stays valid until it expires. It is the most precise option - it removes one principal's access without affecting any other - and is recommended for routine use where such a list exists.
2. **Trust Bundle rotation**: the operator removes the compromised trust anchor from the Trust Bundle, invalidating every SVID that chains to it. This is heavy-handed but effective when an entire issuance authority is compromised. See the [Trust Anchor Rotation Playbook](#trust-anchor-rotation-playbook) below, which also covers the case where the issuer is an intermediate CA whose anchor is the root above it.
3. **Expiry**: wait for the SVID to expire. This is viable only with shorter SVID lifetimes.

None of these options is instantaneous. Allowlist removal takes effect promptly only where the verifier re-evaluates its authorization policy per request; a Trust Bundle rotation propagates no faster than the fleet's refresh interval. In either case a long-lived mTLS connection can keep the affected peer authenticated until the connection is re-established (see [session lifetime and re-validation](./tls-requirements.md#session-lifetime-and-re-validation)).

## Trust Anchor Rotation Playbook

Rotating a Trust Domain's trust anchor is routine CA lifecycle. This playbook is informative operator guidance; the normative rule it relies on is the [X.509-SVID validation](./svids.md#x509-svid-validation) rule that a verifier accepts an SVID chaining to any anchor in the current Trust Bundle. That is what lets a bundle carry the old and new anchors together during an overlap. Because a verifier only learns about anchor changes when it refreshes the Trust Bundle (see [Trust Bundle retrieval endpoint](./trust-bundle-and-discovery.md#trust-bundle-retrieval-endpoint)), sequence a rotation so that no principal is asked to validate, or authenticate with, material its peers have not yet learned to trust:

1. **Publish both anchors.** Add the new trust anchor to the Trust Bundle alongside the old one and publish the updated bundle.
2. **Wait for propagation.** Allow every verifier to refresh the bundle before proceeding: at least the longest refresh interval in use across the fleet, extended to cover realistic offline windows for intermittently connected principals. Setting the bundle's `spiffe_refresh_hint` (see [selecting and refreshing the bundle](./trust-bundle-and-discovery.md#selecting-and-refreshing-the-bundle)) puts every principal on the same refresh interval, so this wait has one known value to measure against.
3. **Switch issuance.** Issue new SVIDs (and renewals) so they chain to the new anchor. SVIDs that chain to the old anchor remain valid and keep validating, because both anchors are in the bundle.
4. **Retire the old anchor.** Remove the old anchor from the bundle only once no SVID still chains to it: after all principals have renewed, or after the last old SVID has expired. Removing it earlier revokes every remaining SVID that chains to it (which is exactly the intent when rotation is used for compromise response, and an outage otherwise).

Where the MIS operates as an intermediate CA beneath an enterprise or offline root (see the [MIS deployment patterns](./identity-framework.md#deployment-patterns-informative)), the trust anchor in the bundle is that root, not the issuing intermediate. Rotation and bundle-level revocation then act at the root: replacing an intermediate issuer under an unchanged root needs no bundle change and does not follow this playbook, while removing the root anchor invalidates every SVID chaining through it, not only those from one intermediate.

## SVID Lifetime Guidance

MIAF favours short SVID lifetimes: short lifetimes keep the blast radius low and let expiry double as revocation. The right value depends on the principal. A workload identity in a connected service can renew hourly; a device with intermittent or air-gapped connectivity needs enough margin to renew before a realistic offline window ends. As a rough orientation, automated SPIRE-style workload SVIDs are commonly 1-24 hours, while long-lived device SVIDs are often weeks to a few months.

Manual provisioning makes short lifetimes operationally expensive, so an operator relying on it MAY use longer lifetimes than automated renewal would allow. Treat any such extension as a bridge: once automated renewal is available, an operator SHOULD reduce lifetimes to the shortest value compatible with their principals' connectivity.
