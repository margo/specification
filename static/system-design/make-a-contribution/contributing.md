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

Bug and security fixes are _always_ welcome and take the highest priority, see our [Security Policy](https://github.com/margo/specification/blob/pre-draft/SECURITY.md).

## Contribution Checklist

- Contributions to the Specification must be covered by a Corporate CLA or Individual CLA  
- Any code changes must be accompanied with automated tests 
- Add the required copyright header to each new file introduced if appropriate, see [licensing information](https://github.com/margo/specification/blob/pre-draft/LICENSE)
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

## Documentation Generation Process

Some of the resources being used in the Margo APIs are being manually specified using MarkDown files.
In this case `mkdocs` is used to generate the documentation in HTML format.

But for some others the modeling language [LinkML](https://linkml.io/) is being used to generate the documentation.
In this case `linkml` is used to generate the MarkDown documents that are integrated with the above mentioned documents before `mkdocs` can generate the HTML documents.

### Preparation

There are multiple different possibilities to cover as many user set-ups as possible:

- [Development Containers](https://containers.dev/)
- [Python Poetry](https://python-poetry.org/)
- [Python PIP](https://pypi.org/project/pip/)
- Others might or might not work out of the box

#### Development Containers

This repository provides a Development Container (AKA dev-container) that is automatically recognized by VsCode.

It is out of the scope of this project to document how to use Development Containers, please visit <https://containers.dev/> to help yourself.

The provided dev-container includes all dependencies.
Therefore, once the Development Container has been activated, the preparation is done.

#### Python Poetry

Python Poetry is a widely used tool for dependency management in the Python ecosystem.

It is out of the scope of this project to document how to use Python Poetry, please visit <https://python-poetry.org/> to help yourself.

One feature of Poetry (also available in some of the other tools) very important for the reliability of the generation process is the possibility of easily "freezing" the dependencies and installing them in Python virtual environments (AKA _venv_s).
Poetry is being used in the pipeline that generates the documentation for a more reliable process (thanks to its reproducibility).

Poetry v2 is required to ensure that the same dependencies specification file can be also used with other tools (like PIP), thanks to its conformance with [PEP-518](https://peps.python.org/pep-0518/).

In order to install the dependencies, simply run `poetry install` from the top directory of this repository.
With this the preparation is done.

#### Python PIP

Python PIP is the most basic dependency manager in the Python ecosystem and is therefore available almost in all Python installations.

It is out of the scope of this project to document how to use Python PIP, please visit <https://packaging.python.org/en/latest/tutorials/installing-packages/> to help yourself.

In order to install the dependencies, simply run `pip install <pyproject.toml path>`, being _<pyproject.toml path>_ the path to the file under that name provided in the top directory of this repository.
With this the preparation is done.

### Generation of the Documentation

Once the required tools have been installed as documented in the [Preparation](#preparation) section, these tools can be used to:

1. [Optional] [Only for LinkML specified resources] Validate the input for the MarkDown document generation.
2. [Only for LinkML specified resources] Generate all the needed MarkDown documents.
3. Generate the HTML documents.

As mentioned in a previous section, as of now only some of the resources are being specified in LinkML and are being used to generate the MarkDown documents.
Steps 1. and 2. only apply to those documents.

Currently two Bash scripts are being provided the directory `doc-generation` to simplify steps 1. and 2.

The input for the generation of the MarkDown documents is provided in the directory `./src/`.

#### Validate input for MarkDown Generation

The script `check-examples.bash` locationed in the following location `./doc-generation/check-examples.bash`` checks:

- the validity of the LinkML resource definitions (AKA schemas), and
- the validity of provided examples and counter-examples according the resource definitions

"Counter-examples" are examples that should be recognized as invalid, when checked against the resource definitions.

#### Generate MarkDown Documents

The script `generate-documentation.bash` located in the followign location `./doc-generation/generate-documentation.bash` generates MarkDown documents for the resources specified in LinkML format.

The LinkML specification documents can be found in the directory `./src/` and the resulting MarkDown documents are integrated with the other MarkDown documents in the directory `/system design/`.

#### Generate HTML Documents

The documentation gets converted into HTML for public availability using `mkdocs`.

MkDocs cannot only convert MarkDown documents into HTML documentation (using `mkdocs build`), but is can also start a webserver (using `mkdocs serve`) for local rendering of the documentation on a web browser.

### Other information

Each resource description has a responsible person which can decide to use LinkML to generate the MarkDown documentation or to write the MarkDown documentation manually.

Transforming a manually written MarkDown document into one generated out of LinkML is not a one-direction road.
Going back to manually written (or generated differently) MarkDown documents is as easy as committing the MarkDown documents generated out of LinkML and disabling the generation.
