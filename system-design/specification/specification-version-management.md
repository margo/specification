# Version Management Strategy
## Purpose

The purpose of this document is to explain the Margo initiatives version management strategy. This version management outline covers the major deliverables the Margo initiative is responsible for.

The goal is to make public releases easy to understand, keep preview builds useful for feedback, and ensure all official deliverables can be versioned together at release.

## Versioning Approach

Margo intends to use one public semantic version for the official Margo release(s) and apply it to these deliverables at release time:

Current Preview Release deliverables include:
- Specification
- Open API Specification(s)
- Code first sandbox

The following will be delivered at the time of our first General Release 1:
- Reference Implementation
    - includes various software components
- Conformance Test Toolkit(CTT)
    - includes various software components

The specification remains the release anchor. The other three deliverables inherit the same public version when they are published as part of the same official release.

This keeps the release story simple:

- Preview work can happen frequently without creating misleading public version jumps
- Public releases only increment one semantic version field at a time
- All official deliverables for a given release are clearly compatible with each other

## Versioning Model

### General Availability(GA) release versions

Official releases should use plain semantic versioning:

- `1.0.0`
- `1.0.1`
- `1.1.0`
- `2.0.0`

The release number should advance based on the highest level of accepted change since the previous public release:

| Change in release scope | Next public version | Rule |
| --- | --- | --- |
| Clarifications, corrections, non-breaking fixes only | PATCH | `1.0.0 -> 1.0.1` |
| One or more non-breaking additions or new features | MINOR | `1.0.0 -> 1.1.0` |
| One or more breaking changes | MAJOR | `1.0.0 -> 2.0.0` |

When multiple change types exist, the release should use the highest-precedence change type:

- Major supersedes minor
- Minor supersedes patch
- Patch does not increment if a minor or major release is already required

> Note: SemVer itself defines what major, minor, and patch mean, but this precedence rule is a release management policy built on top of those semantics.

### Preview Release(PR) deliverables before release

Preview release deliverables should use preview release labels instead of incrementing the public semantic version for every change implemented.

These PR deliverables are not official releases of the specification. They are incremental checkpoints that show the suppliers/community what is being prepared for the next official release.

Margo plans to publish preview releases quarterly on the 15th day of each quarter-end month:

- March 15
- June 15
- September 15
- December 15

The version semantics documented in this plan still apply to each preview release. The scheduled quarterly release determines when a preview is published, not how the semantic version is classified.

The single pre-release label used across all stages is `rc.N`. The branch the tag lives on and the base version number together provide the stage context.

Examples:

- `1.0.0-rc.1`
- `1.0.0-rc.7`
- `1.1.0-rc.1`

The base semantic version in the preview tag should represent the next intended public release. That means:

- Before the first official release, preview versions target `1.0.0`
- After `1.0.0` is released, if the next release is expected to be a non-breaking feature release, previews move to `1.1.0-rc.1`
- If later work introduces a breaking change, previews move to `2.0.0-rc.1`

This preserves semantic meaning while still allowing frequent preview publication without treating each internal change as a released specification version.

## Deliverable Plan

### Specification & Documentation

The Specification and supporting documentation is the authoritative driver for release classification.

- `rc.N` represents all pre-release working snapshots regardless of branch stage
- Final publication removes the suffix and publishes the plain semantic version

Release decisions for patch, minor, or major should be based on specification impact:

- `Patch` for clarifications, corrections, and non-breaking wording updates
- `Minor` for new non-breaking capabilities or normative additions
- `Major` for normative breaking changes

### OpenAPI specification

The OpenAPI specification should share the same public release version as the specification because it describes the same release contract.

- Preview versions should mirror the specification version exactly
- Final GA release should publish the same semantic version as the specification
- If the OpenAPI document changes in a way that changes the contract, that change must be considered in the release classification

Examples:

- Spec `1.1.0-rc.2` -> OpenAPI `1.1.0-rc.2`
- Spec `1.1.0` -> OpenAPI `1.1.0`

### Reference Implementation

The reference implementation shares the specification's major and minor version at initial release. After that, the patch number may be incremented independently for software-only fixes such as critical bugs or security issues, without requiring a specification change.

- **Major and minor** versions must match the specification version being implemented
- **Patch** version may differ to accommodate software-only releases (bug fixes, security patches)
- Preview builds use the same target semantic version with `rc` labels
- Implementation-only iteration between previews should increase the pre-release sequence

Examples:

- Specification target `1.1.0-rc.4` -> Reference implementation `1.1.0-rc.4`
- Initial release aligned to spec `1.1.0` -> Reference implementation `1.1.0`
- Security patch to reference implementation only -> Reference implementation `1.1.1` (spec remains `1.1.0`)

If the reference implementation uncovers a breaking issue in the specification, the release classification should be revised before the next preview or release is published.

### Conformance test and toolkit

The conformance suite validates one specification release at a time. It shares the specification's major and minor version at initial release. The patch number may be incremented independently for software-only fixes after the initial release.

- **Major and minor** versions must match the specification release the toolkit validates
- **Patch** version may differ for bug fixes, tooling updates, or security patches not related to specification changes
- Preview versions follow the same pre-release label sequence as the specification
- Toolkit updates that change expected test behavior must feed back into release classification before GA

Examples:

- Conformance test for spec `1.0.0-rc.3` -> toolkit `1.0.0-rc.3`
- Initial toolkit release for GA spec `1.0.0` -> toolkit `1.0.0`
- Bug fix to toolkit only -> toolkit `1.0.1` (spec remains `1.0.0`)

If the CTT uncovers a breaking issue in the specification, the release classification should be revised before the next preview or release is published.

## Release Cohesion Rule

At an official release, all four Margo deliverables publish with the same version number. After the initial release, the specification and OpenAPI specification continue to version in lockstep, while the reference implementation and conformance toolkit may increment their patch version independently for software-only changes.

### At initial release — all deliverables share the same version

| Deliverable | Version at GA example |
| --- | --- |
| Specification | `1.1.0` |
| OpenAPI specification | `1.1.0` |
| Reference implementation | `1.1.0` |
| Conformance test and toolkit | `1.1.0` |

### After release — software patch versions may diverge

The major and minor versions must remain in sync with the specification. Only the patch number may differ, and only for software-only fixes (bugs, security issues, tooling).

| Deliverable | Version after independent patches |
| --- | --- |
| Specification | `1.1.0` |
| OpenAPI specification | `1.1.0` |
| Reference implementation | `1.1.2` |
| Conformance test and toolkit | `1.1.1` |

A user seeing reference implementation `1.1.2` can immediately determine it implements specification `1.1.x`. Any new feature or breaking change must be tied to a specification change, which would increment the minor or major version and realign all deliverables at the next coordinated release.

## Estimated Workflow

### Phase 1: Pre-draft work

- Publish working previews as `X.Y.Z-rc.N` on the pre-draft branch
- Target quarterly preview publication on March 15, June 15, September 15, and December 15
- Increment `N` for each quarterly drop or agreed checkpoint
- Use issue and branch tags to track PR numbers or work items instead of embedding PR identifiers in the semantic version

### Phase 2: Draft review

- Promote pre-draft content to the draft branch when the working group is ready for broader review
- Continue using `X.Y.Z-rc.N` on the draft branch, incrementing `N` as draft issues are resolved
- Continue using the quarterly preview publication target unless an exception is approved
- Restrict changes to issues that still affect release readiness

### Phase 3: Coordinated release validation

- Assemble the specification, OpenAPI specification, reference implementation, and conformance toolkit on the same target version
- Publish a final `X.Y.Z-rc.N` tag on the draft branch to mark the validated release candidate
- Validate that all four deliverables still align to the same contract

### Phase 4: Official release

- Publish the plain semantic version with no suffix
- Release all four official deliverables on that same version number
- Publish release notes that explain whether the release is patch, minor, or major and why

## Git Tagging Strategy

Each quarterly preview publication uses two independent Git tags applied to the repository. These tags are separate identifiers that can point to the same commit or to different commits depending on what is needed for a given event.

### Quarterly release tag

Every quarterly drop receives a semantic version tag that follows the pre-release label scheme defined in this document:

- Format: `vX.Y.Z-rc.<N>`
- Examples: `v1.0.0-rc.1`, `v1.0.0-rc.2`, `v1.1.0-rc.1`

This tag marks the official state of the specification at that quarterly checkpoint. It is the version consumers and implementers reference when tracking which preview they are working against.

### Event-specific tag

When a specific commit needs to be identified for an external event (such as a plugfest), a separate human-readable tag is applied independently of the quarterly release tag:

- Format: `<event>-<YYYY-MM>` or `<event>-<YYYY-MM-DD>`
- Examples: `plugfest-2026-07`, `plugfest-2026-07-15`

This tag provides a stable, memorable reference for the exact commit used at that event. It does not need to coincide with a quarterly release tag — organizers can point participants to this tag without changing the semantic version history.

### Why two tags

Keeping the tags independent provides flexibility:

- The quarterly release tag preserves the semantic version record and drives the versioning story for implementers
- The event tag can be placed on any commit — including a hotfix applied after the quarterly drop — without creating an unplanned version increment
- Participants at an event receive one clear, unambiguous identifier to check out regardless of how many quarterly iterations have occurred

### Example

For PR2 with a plugfest in July 2026:

| Purpose | Tag |
| --- | --- |
| Quarterly preview release | `v1.0.0-rc.2` |
| Plugfest reference commit | `plugfest-2026-07` |


## Branching Strategy

The branching model maps directly to the four stages defined in the membership agreement: **pre-draft → draft → final approval → publication**.

### Branch layout

- **`pre-draft`** — active working branch for ongoing contributions. Always targets the next+1 public version relative to whatever is currently in draft.
- **`draft`** — branch that receives content once the working group votes to advance from pre-draft. Targets the next public version.
- **`release`** (or `main`) — receives the final merge once the working group reaches final approval. Carries the plain semantic version with no suffix at publication.

Changes flow **down only**: if a correction is needed while content is in the draft branch, the fix is made in draft and merged down into pre-draft — not the reverse.

### Version progression across branches

After a `1.0.0` GA publication, the three long-lived branches carry these versions:

| Branch | Version | Stage |
| --- | --- | --- |
| `release` | `1.0.0` | Published |
| `draft` | `1.1.0-rc.#` | Draft review — work heading toward next release |
| `pre-draft` | `1.2.0-rc.#` | Pre-draft — work heading toward next+1 release |

### Promotion mechanics

When the working group votes to advance pre-draft content into draft:

1. The draft branch receives the merge and **continues with the same version number** that was on pre-draft (for example, `1.1.0-rc.3` remains `1.1.0-rc.3` in draft).
2. The pre-draft branch is **incremented to the next+1 target version** (for example, pre-draft moves from `1.1.0-rc.3` to `1.2.0-rc.1`).

This means pre-draft always reflects a higher target version than draft, making it immediately clear which branch represents which upcoming release.

Each quarterly drop increments `N` on the appropriate branch. Once the draft branch reaches final approval, it merges to release and the suffix is dropped, publishing the plain semantic version.

### Repositories requiring this branch structure

- Specification
- General website content
- Conformance documentation(coming soon)
- Reference Implementation(coming soon)

## Sandbox Relationship

The sandbox should keep its own release cycle, as described in [Sandbox Release Document](https://github.com/margo/sandbox/blob/main/docs/release.md). It is a supporting implementation environment to enable the code first process, not the authoritative version anchor for the specification.

Recommended relationship:

- Sandbox implementation depends on the OpenAPI spec within the specification. Changes to specification should be reflected in the sandbox at the next convenient release. 
- Sandbox retains its own SemVer and release automation
- Sandbox release notes should state which specification release they align to
- Sandbox tags may use release candidates and nightly builds independently of the specification deliverables
- Sandbox changes do not force a specification version bump unless they reflect an accepted specification change

Example compatibility statement:

- Sandbox `v0.8.0` aligns with Margo release `1.1.0`

This preserves the useful sandbox process from the existing release document without coupling sandbox cadence to specification governance.