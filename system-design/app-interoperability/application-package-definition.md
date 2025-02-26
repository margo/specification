# Application Package Definition

The application package, which is used to [distribute an application](../margo-overview/application-package-overview.md), comprises the following elements:
 
- The **application description**: a YAML document with the element `kind` defined as `ApplicationDescription`, which is stored in a file (for example named `margo.yaml`) and contains information about the application's [metadata](../margo-api-reference/workload-api/application-package-api/application-description.md#metadata-attributes) (e.g., description, icon, release notes, license file, etc.), application supported [deployment configurations](../margo-api-reference/workload-api/application-package-api/application-description.md#deploymentprofile-attributes) (e.g,  Helm charts, Compose package), and [configurable application parameters](../margo-api-reference/workload-api/application-package-api/application-description.md#defining-configurable-application-parameters).  There SHALL be only one YAML file in the package root of kind `ApplicationDescription`.
- The **resources**, which are additional information about the application (e.g., manual, icon, release notes, license file, etc.) that can be provided in an [application catalog](../margo-overview/technical-lexicon.md) or [marketplace](../margo-overview/technical-lexicon.md).

The application package has the following file/folder structure:

```yaml
/                           # REQUIRED top-level directory 
└── application description # REQUIRED a YAML document with element 'kind' as 'ApplicationDescription' stored in a file  (e.g., 'margo.yaml')
└── resources               # OPTIONAL folder with application resources (e.g., icon, license file, release notes) that can be displayed in an application catalog
```

An application aggregates one or more [OCI Containers](https://github.com/opencontainers). While the application package is made available in an [application registry](./workload-orch-to-app-reg-interaction.md), the referenced OCI artifacts are stored in a remote or [local registry](../app-interoperability/local-registries.md). 

> **Note**  
> Application catalogs or marketplaces are out of scope for Margo. The exact requirements of the marketing material shall be defined by the application marketplace beyond outlined mandatory content.

The [deployment profiles](../margo-api-reference/workload-api/application-package-api/application-description.md#deploymentprofile-attributes) specified in the application description SHALL be defined as Helm Charts AND/OR Compose components.

- To target devices, which run Kubernetes, applications must be packaged as Helm charts using [Helm (version 3)](https://helm.sh/docs/topics/charts/).
- To target devices, which deploy applications using [Compose](https://www.compose-spec.io/), applications must be packaged as a tarball file containing the *compose.yml* file and any additional artifacts referenced by the Compose file (e.g., configuration files, environment variable files, etc.). It is highly recommend to digitally sign this package. When digitally signing the package PGP encryption MUST be used.

> **Investigation Needed**: We plan to do a security review of this package definition later.
> During this review we will revisit the way the Compose tarball file should be signed.
> We will also discuss how we should handle secure container registries that require a username and password.
>
> **Investigation Needed**: We need to determine what impact, if any, using 3rd party helm charts has on being Margo compliant.
>
> **Investigation Needed**: Missing in the current specification are ways to define the compatibility information (resources required to run, application dependencies) as well as required infrastructure  services  such as storage, message queues/bus, reverse proxy, or authentication/authorization/accounting.

If either one cannot be implemented it MAY be omitted but Margo RECOMMENDS defining [deployment profiles](../margo-api-reference/workload-api/application-package-api/application-description.md#deploymentprofile-attributes) as both Helm chart **AND** Compose components to strengthen interoperability and applicability.

> **Note**
> A device running the application will only install the application using either Compose files or Helm Charts but not both.

## Relevant Links
Please follow the subsuquent link to view the technical reference:

- [Application Description](../margo-api-reference/workload-api/application-package-api/application-description.md)
