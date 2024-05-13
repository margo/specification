# Application Package Definition

This section addresses how an application is packaged by the “App Developer” who has implemented the application and aims to provide it to Margo-conformant systems. An application aggregates one or multiple [OCI Containers](https://github.com/opencontainers). The **application package** is made available in an [application registry](./workload-orch-to-app-reg-interaction.md).  

The application package comprises (a) the **application description** file `margo.yaml`, which contains informative contents and metadata (e.g., for application discovery purposes), (b) the **application manifests** ([Helm Chart](https://helm.sh/docs/) and [Docker Compose](https://github.com/compose-spec/compose-spec/blob/master/03-compose-file.md)) containing deployment instructions, and optionally (3) **application resources** (e.g., container binaries), which are necessary to enable the lifecycle of the application.

The application manifest SHALL be defined as a Helm Chart AND/OR a Docker Compose. If either one cannot be implemented it MAY be omitted.  

Margo RECOMMENDS defining both (Helm Chart **AND** Docker Compose) for strengthening interoperability and applicability.  

A device that runs the application can only actively run either Docker Compose or Helm Chart.

## Application Package Structure

The application package has the following folder structure:

```yaml
/                            # REQUIRED top-level directory 
└── margo.yaml               # REQUIRED application description file in YAML Format 
└── resources                # OPTIONAL folder with e.g., container binaries 
└── manifest                 # REQUIRED folder containing the application manifest 
    ├── helm-chart           # OPTIONAL: Helm chart (or reference to it) goes in this folder  
        ├── Chart.yaml 
        ├── charts 
        │   └── ... 
        ├── templates 
        │   └── ... 
        └── values.yaml 
    └── docker-compose       # OPTIONAL: Docker Compose file goes in this folder 
        └── compose.yaml
```

## Application Description

The `margo.yaml` file is the application description. The purpose of this file is to present the application on an [application registry](./workload-orch-to-app-reg-interaction.md) or marketplace from where an end user selects the application to hand it over to the Workload Orchestration Software, which configures it and makes it available on the “app repo” for installation on the edge device (see Section [Workload Orchestration Agent](./workload-orchestration-agent.md)).

> **Note**
> The format of the application description is *inspired by* the [Open Application Model](https://github.com/oam-dev/spec) (OAM), however, the format defined here is a *narrow subset*, which is sufficient for the goals of the Margo specification at this point.

**Application Description Example**

An example of an `margo.yaml` file is shown below:

```yaml
apiVersion: margo.dev/v1 
kind: application 
metadata: 
  name: my-helm-nginx-margo-app 
  version: 0.1.0 
  description: Example of packaging nginx as a Margo application.
  icon: "./resources/nginx-logo-s.png" 
  author: John Smith 
  organization: App Devs Inc. 
  organization-site: https://app-devs.com 
  app-tagline: My cool example app. 
  description-long: Long description of my cool app ... 
  license-file: "./resources/LICENCE.txt" 
  app-site: https://my-cool-app.com 
spec: 
  helm-chart: 
    repoType: local
    url: "./manifest/helm-chart" 
  docker-compose: 
    repoType: local 
    url: "./manifest/docker-compose/compose.yaml" 
```

**Top-level Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| apiVersion      | string    | Y    | Identifier of the version of the API the object definition follows.|
| kind            | string    | Y    | Must be `application`.|
| metadata        | Metadata    | Y    | Metadata element specifying characteristics about the application. See the [Metadata](#metadata-attributes) section below. |
| spec            | Spec    | Y    | Spec element that defines components of the application. See the [Spec](#spec-attributes) section below. |

**Metadata Attributes**

| Attribute        | Type            | Required?       | Description     |
|------------------|-----------------|-----------------|-----------------|
| name             | string          | Y    | The name of the name of the application.|
| version          | string          | Y    | Version of the application.|
| description      | string          | Y    | Short application description summary. |
| release-notes    | string          | N    | Statement about changes of this release of the application.  |
| icon             | string          | N    | Link to the icon file (e.g., in PNG format).  |
| author           | string          | N    | Person who created the application. |
| author-email     | string          | N    | Email address of person who created the application.  |
| organization     | string          | Y    | Organization that is responsible for the application development. |
| organization-site| string          | N    | Link to the organization website.  |
| app-tagline      | string          | N    | A brief statement about the application.  |
| description-long | string          | N    | A long description about the application.  |
| license-file     | string          | N    | Link to the file that details the license of the application.|
| app-site         | string          | N    | Link to the application website. |

**Spec Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| helm-chart      | DeploymentDef       | Y    | Details on the Helm Chart deployment definition of the application. See the [DeploymentDef](#deploymentdef-attributes) section below.|
| docker-compose  | DeploymentDef       | Y    | Details on the Docker Compose deployment definition of the application. See the [DeploymentDef](#deploymentdef-attributes) section below. |

**DeploymentDef Attributes**

| Attribute       | Type            | Required?       | Description     |
|-----------------|-----------------|-----------------|-----------------|
| repoType        | string          | Y               | The type of repository where the deployment definition can be found. Options are: http, git, local. |
| url             | string          | Y               | The URL to the deployment definition. In case of 'docker-compose', the URL points at the `compose.yaml` file.|

> **Note**  
> Missing in the current specification are ways to define the compatibility information (resources required to run, application dependencies) as well as required infrastructure  services  such as storage, message queues/bus, reverse proxy, or authentication/authorization/accounting.

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
