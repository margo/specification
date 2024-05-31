# Application Package Definition

This section addresses how an application is packaged by the “Application Developer” who has implemented the application and aims to provide it to Margo-conformant systems. An application aggregates one or more [OCI Containers](https://github.com/opencontainers). The **application package** is made available in an [application registry](./workload-orch-to-app-reg-interaction.md).  

The application package comprises:

- The **application description** file `margo.yaml`, which contains information about the application's marketing details (e.g., description, icon, release notes, license file, etc.), resource requirements, required input parameters, and application's installation packages (e.g,  Helm charts, docker-compose package) location.
- The **application resources** which can be used to display additional information about the application in an application catalog or marketplace based on the application's defined metadata (e.g., description, icon, release notes, license file, etc.).

The application package sources SHALL be defined as Helm Charts AND/OR a Docker Compose packages.

- To target devices running Kubernetes applications must be packaged as helm charts using [Helm V3](https://helm.sh/).
- To target devices deploying applications using Docker Compose files you must create a tarball file containing the application's docker-compose.yml file and any additional artifacts referenced by the docker compose file (e.g., configuration files, environment variable files, etc.). It is highly recommend to digitally sign this package. When digitally signing the package PGP MUST be used.

> **Investigation Needed**: We plan to do a security review of this package definition later.
> During this review we will revisit the way the docker compose tarball file should be signed.
> We will also discuss how we should handle secure container registries that require a username and password.

If either one cannot be implemented it MAY be omitted but Margo RECOMMENDS defining sources for both Helm Chart **AND** Docker Compose source packages to strengthen interoperability and applicability.

> **Note**
> A device running the application will only install the application using either Docker Compose files or Helm Charts but not both.

## Application Package Structure

The application package has the following folder structure:

```yaml
/                            # REQUIRED top-level directory 
└── margo.yaml               # REQUIRED application description file in YAML Format 
└── resources                # OPTIONAL folder with application catalog resources e.g., icon, license file, release notes 
```

## Application Description

The `margo.yaml` file is the application description. The purpose of this file is to present the application on an application catalog or marketplace from where an end user selects the application to hand it over to the Workload Orchestration Software, which configures it and makes it available for installation on the edge device (see Section [Workload Orchestration Agent](./workload-orchestration-agent.md)).

**Application Description Example**

A simple hello-world example of an `margo.yaml` file is shown below:

```yaml
apiVersion: margo.org/v1-alpha1
kind: application
metadata:
  id: com.northstartida.hello.world
  name: Hello World
  description: A basic hello world application
  version: 1.0
  catalog:
    application:
      icon: ./resources/hw-logo.png
      tagline: Northstar Industrial Application's hello world application.
      descriptionFile: ./resources/description.md
      releaseNotes: ./resources/release-notes.md
      licenseFile: ./resources/license.pdf
      site: http://www.northstar-ida.com
    author:
      - name: Roger Wilkershank
        email: rpwilkershank@northstar-ida.com
    organization:
      - name: Northstar Industrial Applications
        site: http://northstar-ida.com
sources:
  cluster:
    - name: hello-world
      type: helm.v3
      properties:  
        repository: oci://northstarida.azurecr.io/charts/hello-world
        revision: 1.0.1
        wait: true
```

An example of a `margo.yaml` file using multiple helm charts and a docker-compose file package is shown below.

```yaml
apiVersion: margo.org/v1-alpha1
kind: application
metadata:
  id: com.northstartida.digitron.orchestrator
  name: Digitron orchestrator
  description: The Digitron orchestrator application
  version: 1.2.1 
  catalog:
    application:
      icon: ./resources/ndo-logo.png
      tagline: Northstar Industrial Application's next-gen, AI driven, Digitron instrument orchestrator.
      descriptionFile: ./resources/description.md
      releaseNotes: ./resources/release-notes.md
      licenseFile: ./resources/license.pdf
      site: http://www.northstar-ida.com
    author:
      - name: Roger Wilkershank
        email: rpwilkershank@northstar-ida.com
    organization:
      - name: Northstar Industrial Applications
        site: http://northstar-ida.com
sources:
  cluster:
    - name: digitron-orchestrator
      type: helm.v3
      properties:
        repository: oci://northstarida.azurecr.io/charts/northstarida-digitron-orchestrator
        revision: 1.0.9
        wait: true
    - name: database-services
      type: helm.v3
      properties: 
        repository: oci://quay.io/charts/realtime-database-services
        revision: 2.3.7
        wait: true
  standalone:
    - name: digitron-orchestrator-docker
      type: docker-compose
      properties:
        packageLocation: https://northsitarida.com/digitron/docker/digitron-orchestrator.tar.gz
        keyLocation: https://northsitarida.com/digitron/docker/public-key.asc
```

**Top-level Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string          | Y               | Identifier of the version of the API the object definition follows.|
| kind            | string          | Y               | Must be `application`.|
| metadata        | Metadata        | Y               | Metadata element specifying marketing characteristics about the application. See the [Metadata](#metadata-attributes) section below.|
| sources         | Source        | Y               | Source element specifying the software packages to install. See the [Source](#source-attributes) section below. |

**Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| id               | string          | Y    | An identifier for the application. The id is used to help create unique identifiers where required, such as namespaces. It must be in reverse domain name notation.|
| name             | string          | Y    | The application's official name.|
| version          | string          | Y    | The application's version.|
| catalog          | Catalog         | Y    | Catalog element specifying the application catalog details used to display the application in an application catalog or marketplace. See the [Catalog](#catalog-attribute) section below.|

**Catalog Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| application      | Application     | N               | Application element specifying the application specific metadata. See the [Application Metadata](#application-metadata-attributes) section below.|
| author           | []Author          | N               | Author element specifying metadata about the application's author. See the [Author Metadata](#author-metadata-attributes) section below.|
| organization     | []Organization    | Y               | Organization element specifying metadata about the organization/company providing the application. See the [Organization Metadata](#organization-metadata-attributes) section below.|

**Application Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| descriptionFile  | string          | N               | Link to the file containing the application's full description. The file should be a markdown file.|
| icon             | string          | N               | Link to the icon file (e.g., in PNG format).|
| licenseFile      | string          | N               | Link to the file that details the application's license. The file should either be a plain text, markdown or PDF file.|
| releaseNotes     | string          | N               | Statement about the changes for this application's release. The file should either be a markdown or PDF file.|
| site             | string          | N               | Link to the application's website.|
| tagline          | string          | N               | The application's slogan.|

**Author Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| name             | string          | N               | The name of the application's creator.|
| email            | string          | N               | Email address of the application's creator.|

**Organization Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| name             | string          | Y               | Organization responsible for the application's development and distribution.|
| site             | string          | N               | Link to the organization's website.|

**Source Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| cluster          | []SourceType    | N               | Source type element for indicating the source for deploying the application on a cluster using Helm. See the [Source Type](#source-type-attributes) section below. |
| standalone      | []SourceType    | N               | Source type element for indicating the source for deploying the application on a standalone device using Docker compose. See the [Source Type](#source-type-attributes) section below. |

**Source Type Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| name             | string          | Y               | A unique name used to identify the package source. For helm installations the name will be used as the chart name. |
| type             | string          | Y               | Indicates the source's package format. The values are `helm.v3` to indicate the source's package format is Helm version 3 and `docker-compose` to indicate the source's package format is Docker Compose. When installing the application on a device supporting the Kubernetes platform all `helm.v3` sources, and only `helm.v3` sources, will be provided to the device in same order they are listed in the application description file. When installing the application on a device supporting docker-compose all `docker-compose` sources, and only `docker-compose` sources, will be provided to the device in the same order they are listed in the application description file. The device will install the sources in the same order they are listed in the application description file. Source types under `cluster` must use `helm.v3`. Source types under `standalone` must use `docker-compose` |
| properties      | SourceProperty | Y                | SourceProperty element specifying the details about the source package. See the [Source Property](#source-property-attributes) section below.|

**Source Property Attributes**

**Investigation Needed**: We need to determine what impact, if any, using 3rd party helm charts has on being Margo compliant.

Properties for sources using `helm.v3`

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| repository       | string          | Y               | The URL indicating the helm chart's location.|
| revision         | string          | Y               | The helm chart's full version.|
| wait             | bool            | N               | If `True`, indicates the device MUST wait until the helm chart has finished installing before installing the next helm chart. The default is `True`. The Workload Orchestration Agent MUST support `True` and MAY support `False`. Only applies if multiple `helm.v3` sources are provided.|

Properties for sources using `docker-compose`

> **Investigation Needed**: We need to have more discussion about how docker-compose should be handled and what is required here.

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| packageLocation  | string          | Y               | The URL indicating the Docker Compose package's location. |
| keyLocation      | string          | N               | The public key used to validated the digitally signed package. It is highly recommend to digitally sign the package. When signing the package PGP MUST be used.|
| wait             | bool            | N               | If `True`, indicates the device MUST wait until the Docker Compose file has finished starting up before starting the next Docker Compose file. The default is `True`. The Workload Orchestration Agent MUST support `True` and MAY support `False`. Only applies if multiple `docker-compose` sources are provided.|

> **Note**  
> Missing in the current specification are ways to define the compatibility information (resources required to run, application dependencies) as well as required infrastructure  services  such as storage, message queues/bus, reverse proxy, or authentication/authorization/accounting.
>
> **Note**  
> Application Marketplaces are out of scope for Margo. The exact requirements of the Marketing Material shall be defined by the Application Marketplace beyond outlined mandatory content.

## Application Manifests  

The purpose of the application manifests is to provide all metadata to enable the lifecycle of the application within the edge device via the [Workload Orchestration Agent](./workload-orchestration-agent.md). An application manifest is either defined as a ([Helm Chart](#application-manifest-using-helm-helm-chart) or a [Docker Compose](#application-manifest-using-docker-compose)):

**Application Manifest using Docker Compose**

In this case, the Margo application comprises a deployment definition that is defined by [Docker Compose](https://github.com/compose-spec/compose-spec/blob/master/03-compose-file.md). Therefore, the application description file, `margo.yaml`, contains a `docker-compose` deployment definition in which a Docker Compose configuration file is referenced. Its filename SHOULD be “compose.yaml”, but MAY be any other file name as well. The example [application description file](#application-description-example) illustrates this.

The referenced `./manifest/docker-compose/compose.yaml` file in the [example](#application-description-example) looks like this:  

```yaml
version: 2.4 
services: 
  db: 
    image: mariadb:10.6.4-focal 
    command: '--default-authentication-plugin=mysql_native_password' 
    volumes: 
      - db_data:/var/lib/mysql 
    restart: always 
    mem_limit: 350m 
    environment: 
      - MYSQL_ROOT_PASSWORD=somewordpress 
      - MYSQL_DATABASE=wordpress 
      - MYSQL_USER=wordpress 
      - MYSQL_PASSWORD=wordpress 
    expose: 
      - 3306 
      - 33060 
  wordpress: 
    image: wordpress:php8.3-fpm 
    volumes: 
      - wp_data:/var/www/html 
    ports: 
      - 80:80 
    restart: always 
    mem_limit: 500m 
    environment: 
      - WORDPRESS_DB_HOST=db 
      - WORDPRESS_DB_USER=wordpress 
      - WORDPRESS_DB_PASSWORD=wordpress 
      - WORDPRESS_DB_NAME=wordpress 
volumes: 
  db_data: 
  wp_data: 
```

The execution of this Margo application will entail (1) the copying of the referenced `compose.yaml` file into the local directory foreseen by the Workflow Orchestration Agent and (2) the following Docker Compose command:

```shell
$ docker compose up 
```

> **Note**  
> The supported function set of docker compose might be limited by certain or all Margo-compliant implementations. For example, to reflect security policies, system dependencies or hardware related limitations. This could affect:
> - Supported Docker Compose version number (e.g. max version 2.4) 
> - Unavailability of certain configuration options (e.g. no volumes with absolute paths)
> - Definition range of configuration options (e.g. unavailability of some host port ranges)
> - Mandatory configuration keys (e.g. all services must specify mem_limit)
> - Naming rules (e.g. container names or network names in a specific format)
>
> Uncompliant Docker Compose configurations will be rejected by both the Workload Orchestration Service and the Workload Orchestration Agent.

**Application Manifest using Helm**

Below, the usage of Helm as an application manifest of an Margo application is defined. This can be chosen if the target edge device is running Kubernetes behind the workload orchestration agent. For a full documentation of Helm, we refer to its official [website](https://helm.sh/docs/).

A Helm chart includes the following Helm-specific configuration files and Kubernetes manifest templates:

- Chart.yaml
This file contains metadata about the chart such as name, version, description, and maintainers.
- values.yaml
This file defines the configuration values for the templates. Using this template approach, only this file needs to be changed for deployments in different environments (e.g., development, staging or production).
- templates
This directory contains all Kubernetes manifest files templated to be instantiated with values from the values.yaml file:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - Secrets
  - and other Kubernetes resources.
- charts
This directory may include additional charts that are necessary for the parent chart to function.

> **Note**  
> This version of the Margo specification uses Helm version 3. For additional information refer to the Helm Documentation at [https://helm.sh](https://helm.sh).

An example of a `Chart.yaml` is listed below:

```yaml
apiVersion: v2 
name: my-nginx-0.1.0 
version: 1.0.0 # Version of the chart 
description: Example of packaging nginx as an Margo application. 
type: application  
home: https://my-cool-app.com 
maintainers:   
  - name: John Smith  
    url: https://app-devs.com  
icon: ./resources/nginx-logo-s.png     
appVersion: 0.1.0 
```

An example of a `values.yaml` is listed below:

```yaml
replicaCount: 1 # only 1 pod will be instantiated 
image: 
  repository: nginx 
  pullPolicy: IfNotPresent # will pull image if not already there 
service: 
  protocol: TCP  
  type: ClusterIP # exposes the service on cluster-internal IP 
  port: 80 
resources: 
  limits: # highest limits chart can receive 
     cpu: 0.5   
  requests: # maximum amount of resources chart requests 
     cpu: 0.1 
```

An example of a `deployment.yaml` is listed below:

```yaml
apiVersion: apps/v1 
kind: Deployment 
metadata: 
  name: {{ .Release.Name }}-nginx 
  labels: 
    app: nginx 
spec: 
  replicas: {{ .Values.replicaCount }} 
  selector: 
    matchLabels: 
      app: nginx 
  template: 
    metadata: 
      labels: 
        app: nginx 
    spec: 
      containers: 
        - name: {{ .Chart.Name }} 
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}" 
          imagePullPolicy: {{ .Values.image.pullPolicy }} 
          resources: 
            limits: 
              cpu: "{{ .Values.resources.limits.cpu }}" 
            requests: 
              cpu: "{{ .Values.resources.requests.cpu }}" 
          ports: 
            - name: http 
              containerPort: 80 
              protocol: TCP 
```

An example of a `service.yaml` is listed below:

```yaml
apiVersion: v1 
kind: Service 
metadata: 
  name: {{ .Release.Name }}-service 
spec: 
  selector: 
    app.kubernetes.io/instance: {{ .Release.Name }} 
  type: {{ .Values.service.type }} 
  ports: 
    - protocol: {{ .Values.service.protocol | default "TCP" }} 
      port: {{ .Values.service.port }} 
```

An example of a `configmap.yaml` is listed below:

```yaml
apiVersion: v1 
kind: ConfigMap 
metadata: 
  name: {{ .Release.Name }}-index-html-configmap 
  namespace: default 
data: 
  index.html: | 
    <html> 
    <h1>Welcome</h1> 
    </br> 
    <h1>This is app is Margo-compliant and defined as a Helm Chart.</h1> 
    </html> 
```

## Defining configurable application variables

To allow customers to provide configuration values when installing an application, the `margo.yaml` defines the parameters and configuration sections. This gives the application vendor control over what a custom can configure when installing an application. This also describes how the workload orchestration software vendor must display these parameters to the customer to allow them to specify the values. This also describes how the workload orchestration software vendor must validate the configuration values provided by the customer before the application is installed.

An example of a parameters section in the `margo.yaml` follows here:

```yaml
parameters:  
  sections:  
    - name: General Settings  
      settings:  
        - Name: Greeting  
          value: Hello  
          targets:  
            - key: env.APP_GREETING  
              appliesTo: [“helm-chart”,”docker-compose”]
          description: The greeting to use.  
          schema: requireText  
          dataType: string 
        - name: Greeting Target  
          value: World  
          targets:  
            - key: env.APP_TARGET  
              appliesTo: [“helm-chart”,”docker-compose”]    
          description: The target of the greeting.  
          schema: requireText  
          dataType: string 
  schema:  
    - name: requireText  
      maxLength: 45  
      allowEmpty: false  
```

**Parameters**

This section defines parameters that must be displayed to the user as well as how the workload orchestration software vendor must validate the provided values.

The parameters section is only required if the application requires customers to provide parameter value as part of the installation.

**Parameters Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| section        | map[string]section    | Y | Sections are used to group related parameters together, so it is possible to present a user interface with a logical grouping of the parameters in each section. See the [Section](#section-attributes) section below.|
| schema         | map[string]schema     | N | Schema is used to provide details about how to validate each of the parameter values. At a minimum, the parameter value must be validated to match the parameter’s data type. The schema indicates additional rules the provided value must satisfy to be considered valid input. Schemas only need to be defined for parameters that have additional validation rules other than validating against the data type. See the [Schema](#schema-attributes) section below.|

**Section Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| name            | string     | Y | The name of the section. This may be used in the user interface to show the grouping of the associated parameters within the section. |  
| settings        | settings   | Y | Settings are used to provide instructions to the workload orchestration software vendor for displaying parameters to the customer. See the [Settings](#settings-attributes) section below.  |  

**Settings Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| setting         | map[string]setting    | Y | Defines additional information about each of the parameters to be used in the user interfaces. See the [Setting](#setting-attributes) section below. |  

**Setting Attributes**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| name            | string             | Y | The name of the property to show in the user interface. |  
| value           | string             | N | The property’s default value.  Accepted values are string, integer, double, boolean, array[string], array[integer], array[double], array[boolean]. |
| targets          | map[string]target | Y | Used to indicate which component, and key, the value should be applied to. See the [Target](#target-attributes) section below. |
| description     | string             | Y | A short description of the property. |
| datatype        | string             | Y | Indicates the parameters data type. Accepted values are string, integer, double, boolean, array[string], array[integer], array[double], array[boolean]. |
| schema          | string             | N | The name of the schema definition to use when validating the property value if the property has additional validation rules. See the [Schema](#schema-attributes) section below.|

**Target Attributes**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| key             | string            | Y | The name of the parameter. For Helm, this is the dot notation for the matching element in the `values.yaml` files. For docker-compose, this is the name of the environment variable to set. |  
| appliesTo       | string            | N | Indicates which deployment the parameter value applies to. The valid options are either `helm-chart`, `docker-compose` or both.  |

**Schema Attributes**

The schema indicates the rules each indicated parameter value must meet before using the value to install the application. At a minimum, the provided parameter value must match the parameter’s data type. The value must also be validated against any of the validation rules defined in the schema.

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| name                      | string             | Y | The name of the parameter the configuration setting applies to. |  
| <`validation rule options`> | <*see below*>        | Y | This defines the validation rules to use. The rules are based on the selected input type. |

**Text Validation Rules**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| allowEmpty      | bool              | N | If true, indicates a value must be provided. Default is false if not provided. |  
| minLength       | integer           | N | If set, indicates the minimum number of characters the value must have to be considered valid. |
| maxLength       | integer           | N | If set, indicates the maximum number of characters the value must have to be considered valid. |
| regexMatch      | string            | N | If set, indicates a regular expression to use to validate the value. |

**Boolean Validation Rules**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| allowEmpty      | bool              | N | If true, indicates a value must be provided. Default is false if not provided. |  

**Numeric Integer Validation Rules**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| allowEmpty      | bool              | N | If true, indicates a value must be provided. Default is false if not provided. |  
| minValue        | integer           | N | If set, indicates the minimum allowed integer value the value must have to be considered valid.  |
| maxValue        | integer           | N | If set, indicates the maximum allowed integer value the value must have to be considered valid.  |

**Numeric Double Validation Rules**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| allowEmpty      | bool              | N | If true, indicates a value must be provided. Default is false if not provided. |  
| minValue        | double            | N | If set, indicates the minimum allowed double value the value must have to be considered valid.  |
| maxValue        | double            | N | If set, indicates the maximum allowed double value the value must have to be considered valid.   |
| minPrecision    | integer           | N | If set, indicates the minimum level of precision the value must have to be considered valid.  |
| maxPrecision    | integer           | N | If set, indicates the maximum level of precision the value must have to be considered valid.   |

**Select Validation Rules**

| Attribute       | Type              | Required?       | Description     |
|-----------------|-------------------|-----------------|-----------------|
| allowEmpty      | bool              | N | If true, indicates a value must be provided. Default is false if not provided. |  
| multiselect     | bool              | N | If true, indicates multiple values can be selected. If multiple values can be selected the resulting value is an array of the selected values. The default is false if not provided.   |
| options         | array             | Y | This provides the list of acceptable options the customer can select from. The data type for each option must match the parameter setting’s data type.    |
