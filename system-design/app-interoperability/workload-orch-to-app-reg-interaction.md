# Application Registry

This section describes the Application Registry and the exchange of an [application package](./application-package-definition.md) from an Application Developer to the Workload Orchestration Vendor. 

The Application Developer SHALL use a [Git repository](https://git-scm.com/) to share an [application package](./application-package-definition.md). This Git repository is considered the Application Registry. 

The connectivity between the Workload Orchestration Software and the Application Registry SHALL be read-only. 

Upon installation request from the End User, the Workload Orchestration Vendor SHALL retrieve the [application package](./application-package-definition.md) using a ``git pull`` request from the Application Registry. 

The Workload Orchestration Vendor reads in the application description file, ``margo.yaml``, and presents a user interface that allows the specification of parameters available according to ``margo.yaml``. 

The End User then specifies the configuration parameters for the [application package](./application-package-definition.md). 

Then, the [application package](./application-package-definition.md) is ready to be passed on to the installation process.  

> **Note** 
> The specifics of the installation process are still under discussion: this could be for example a GitOps based approach. 

During this process the containers referenced in the application manifest ([Helm Chart](https://helm.sh/docs/) or [Docker Compose](https://github.com/compose-spec/compose-spec/blob/master/03-compose-file.md)) are retrieved from container/Helm registries. 

At a minimum, a Margo-compliant WOS SHALL provide a way for an end user to manually setup a connection between the WOS and an application registry. This is required so as not to prohibit an end user for being able to install any Margo-compliant application they wish; including applications developed by the end user. 

The Workload Orchestration Vendor MAY provide enhanced user experience options such as the pre-configuring of application registries to monitor. These can include application registries from third-party application vendors or their own applications. 

## Secure Access to the Application Package 

It is expected the connection between the Workload Orchestration software and the Application developer’s application registry is secured using standard secure connectivity best practices. Some standard practices include the following: 

- Basic authentication via HTTPS 
- Bearer token authentication 
- TLS certifications 