# Application Package Definition

This section defines the application package provided by an “Application Developer” who has implemented the application and aims to provide it to Margo-conformant systems. The application package comprises:
 
- The **application description**: a YAML document with the element `kind` defined as `ApplicationDescription`, which is stored in a file (e.g., `margo.yaml`) and contains information about the application's [metadata](#metadata-attributes) (e.g., description, icon, release notes, license file, etc.), application supported [deployment configurations](#deploymentprofile-attributes) (e.g,  Helm charts, Docker Compose package), and [configurable application parameters](#defining-configurable-application-parameters).  There SHALL be only one YAML file in the package root of kind `ApplicationDescription`.
- The **resources**, which are additional information about the application (e.g., manual, icon, release notes, license file, etc.) that can be provided in an [application catalog](../../margo-overview/technical-lexicon) or [marketplace](../../margo-overview/technical-lexicon).

The application package has the following file/folder structure:

```yaml
/                           # REQUIRED top-level directory 
└── application description # REQUIRED a YAML document with element 'kind' as 'ApplicationDescription' stored in a file  (e.g., 'margo.yaml')
└── resources               # OPTIONAL folder with application resources (e.g., icon, license file, release notes) that can be displayed in an application catalog
```

An application aggregates one or more [OCI Containers](https://github.com/opencontainers). While the application package is made available in an [application registry](./workload-orch-to-app-reg-interaction.md), the referenced OCI artifacts are stored in a remote or [local registry](../local-registries). 

> **Note**  
> Application catalogs or marketplaces are out of scope for Margo. The exact requirements of the marketing material shall be defined by the application marketplace beyond outlined mandatory content.

The [deployment profiles](#deploymentprofile-attributes) specified in the application description SHALL be defined as Helm Charts AND/OR Docker Compose components.

- To target devices, which run Kubernetes, applications must be packaged as Helm charts using [Helm V3](https://helm.sh/).
- To target devices, which deploy applications using Docker Compose, applications must be packaged as a tarball file containing the *docker-compose.yml* file and any additional artifacts referenced by the docker compose file (e.g., configuration files, environment variable files, etc.). It is highly recommend to digitally sign this package. When digitally signing the package PGP MUST be used.



## Relevant Links
Please follow the subsuquent links to view more technical information regarding Margo application packaging:

- [Application Package Definition](../app-interoperability/application-package-definition.md)
- [Application Distribution](../app-interoperability/workload-orch-to-app-reg-interaction.md)
