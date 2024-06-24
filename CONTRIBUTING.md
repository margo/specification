# Contributing

This document explains the general requirements on contributions and the recommended preparation steps.
It also sketches the typical integration process.

## New Features

Contributions to Margo are _typically_ very welcome!
However, please keep the following in mind when adding new enhancements:
It is ultimately the responsibility of the maintainers to maintain your addition (although any help is more than appreciated!).
Thus, when accepting new enhancements, we have to make a trade-off between the added value and the added cost of maintenance.
If the maintenance cost exceeds the added value by far, we reserve the right to reject the feature.
Hence it is **recommended to first create a new issue on Github before starting the actual implementation** and wait for feedback from the maintainers.

## Bug Fixes

Bug and security fixes are _always_ welcome and take the highest priority, see our [Security Policy](SECURITY.md).

## Contribution Checklist

- Contributions to the Specification must be covered by a Corporate CLA or Individual CLA  
- Any code changes must be accompanied with automated tests 
- Add the required copyright header to each new file introduced if appropriate, see [licensing information](LICENSE)
- Add `signed-off` to all commits to certify the "Developer's Certificate of Origin", see below
- Structure your commits logically, in small steps
  - one separable functionality/fix/refactoring = one commit
  - do not mix those there in a single commit
  - after each commit, the tree still has to build and work, i.e. do not add
    even temporary breakages inside a commit series (helps when tracking down
    bugs). This also applies to documentation commits processed by, e.g., `mkdocs`
- Base commits on top of latest `pre-draft` branch

### Signing the CLA for Contributions to the Specification
If you have not yet signed the Individual CLA, or your organization has not yet signed the Corporate CLA, or if your account has not yet been authorized by your organization to contribute to Margo, the [LFX EasyCLA bot](https://easycla.lfx.linuxfoundation.org/#/) will prompt you to follow the appriopriate steps to authorize your contribution. 

To ensure your contribution is covered before you make a pull request or to sign the CLA, open a PR at https://github.com/margo/EasyCLA.

### Sign your work

The sign-off is a simple line at the end of the explanation for the patch, e.g.

    Signed-off-by: Random J Developer <random@developer.example.org>

This lines certifies that you wrote it or otherwise have the right to pass it on as an open-source patch.
Check with your employer when not working on your own!

**Tip**: The sign-off will be created for you automatically if you use `git commit -s` (or `git revert -s`).

### Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

        (a) The contribution was created in whole or in part by me and I
            have the right to submit it under the open source license
            indicated in the file; or

        (b) The contribution is based upon previous work that, to the best
            of my knowledge, is covered under an appropriate open source
            license and I have the right under that license to submit that
            work with modifications, whether created in whole or in part
            by me, under the same open source license (unless I am
            permitted to submit under a different license), as indicated
            in the file; or

        (c) The contribution was provided directly to me by some other
            person who certified (a), (b) or (c) and I have not modified
            it.

        (d) I understand and agree that this project and the contribution
            are public and that a record of the contribution (including all
            personal information I submit with it, including my sign-off) is
            maintained indefinitely and may be redistributed consistent with
            this project or the open source license(s) involved.

## Contribution Integration Process

1. Create a pull request on Github.
2. The EasyCLA check, CI pipeline, and other applicable checks as may be introduced must pass.
3. Accepted pull requests are merged into the `pre-draft` branch.
