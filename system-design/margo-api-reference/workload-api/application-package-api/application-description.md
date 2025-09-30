The application description has the purpose of presenting the application, e.g., on an application catalog or marketplace from where an end user selects an application to be installed. The end user defines an `ApplicationDeployment` by specifying [configuration parameters](#defining-configurable-application-parameters) for an `ApplicationDescription`. An `ApplicationDeployment` defines the [desired state](../desired-state-api/desired-state.md) for an application.

### Top-level Attributes

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| apiVersion | string |  Y  | Identifier of the version of the API the object definition follows.|
| kind | string |  Y  | Specifies the object type; must be 'application'.|
| metadata | Metadata |  Y  | Metadata element specifying characteristics about the application deployment. See the [Metadata Attributes](#metadata-attributes) section below.|
| deploymentProfiles | []DeploymentProfile |  Y  | Deployment profiles element specifying the types of deployments the application supports.  See the [Deployment](#deploymentprofile-attributes) section below.|
| parameters | map[string][Parameter] |  N  | Parameters element specifying the configurable parameters to use when installing, or updating, the application. See the [Parameter](#parameter-attributes) section below.|
| configuration | Configuration |  N  | Configuration element specifying how parameters should be displayed to the user for setting the value  as well as the rules to use to validate the user's input.  See the [Configuration](#configuration-attributes) section below.|


### Metadata Attributes  <br><br>
Metadata about the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| id | string |  Y  | An identifier for the application. The id is used to help create unique identifiers where required,  such as namespaces. The id must be lower case letters and numbers and MAY contain dashes.  Uppercase letters, underscores and periods MUST NOT be used. The id MUST NOT be more than 200 characters.|
| name | string |  Y  | The application's official name.  This name is for display purposes only and can container whitespace and special characters.|
| description | string |  N  | None|
| version | string |  Y  | The application's version.|
| catalog | Catalog |  Y  | Catalog element specifying the application catalog details used to display the application  in an application catalog or marketplace.  See the [Catalog](#catalog-attributes) section below.|


### Catalog Attributes  <br><br>
Catalog metadata for displaying the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| application | ApplicationMetadata |  N  | Application element specifying the application specific metadata.  See the [Application Metadata](#applicationmetadata-attributes) section below.|
| author | []Author |  N  | Author element specifying metadata about the application's author.  See the [Author Metadata](#author-attributes) section below.|
| organization | []Organization |  Y  | Organization element specifying metadata about the organization/company providing the application.  See the [Organization Metadata](#organization-attributes) section below.|


### ApplicationMetadata Attributes  <br><br>
Metadata specific to the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| descriptionFile | string |  N  | Link to the file containing the application's full description. The file should be a markdown file.|
| icon | string |  N  | Link to the icon file (e.g., in PNG format).|
| licenseFile | string |  N  | Link to the file that details the application's license. The file should either be a plain text, markdown or PDF file.|
| releaseNotes | string |  N  | Statement about the changes for this application's release. The file should either be a markdown or PDF file.|
| site | string |  N  | Link to the application's website.|
| tagline | string |  N  | The application's slogan.|
| tags | []string |  N  | An array of strings that can be used to provide additional context for the application in a user interface to assist with task such as categorizing, searching, etc.|


### Author Attributes  <br><br>
Information about the application's author. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  N  | The name of the application's creator.|
| email | string |  N  | Email address of the application's creator.|


### Organization Attributes  <br><br>
Information about the providing organization. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  Y  | Organization responsible for the application's development and distribution.|
| site | string |  N  | Link to the organization's website.|


### DeploymentProfile Attributes  <br><br>
Represents a deployment configuration for the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| type | string |  Y  | Defines the type of this deployment configuration for the application.  The allowed values are `helm.v3`, to indicate the deployment profile's format is Helm version 3,  and `compose` to indicate the deployment profile's format is a Compose file.  When installing the application on a device supporting the Kubernetes platform, all `helm.v3` components,  and only `helm.v3` components, will be provided to the device in same order they are listed in the application description file.  When installing the application on a device supporting Compose, all `compose` components,  and only `compose` components, will be provided to the device in the same order they are listed in the application description file.  The device will install the components in the same order they are listed in the application description file.|
| id | string |  Y  | An identifier for the deployment profile, given by the application developer, used to uniquely identify this deployment profile from others within this application description's scope.|
| components | []Component |  Y  | Component element indicating the components to deploy when installing the application.  See the [Component](#component-attributes) section below.|
| description | string |  N  | This human-readable description of a deployment profile allows for providing additional context about the deployment profile. E.g., the application developer can use this to describe the deployment profile's purpose, such as the intended use case. Additionally, the application developer can use this to provide further details about the resources, peripherals, and interfaces required to run the application.|
| requiredResources | RequiredResources |  N  | Required resources element specifying the resources required to install the application.  See the [Required Resources](#requiredresources-attributes) section below. The consequences (e.g., aborting / blocking the installation or execution of the application) of not meeting these required resources are not defined (yet) by margo.|


### RequiredResources Attributes  <br><br>
Required resources element specifying the resources required to install the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| cpu | CPU |  N  | CPU element specifying the CPU requirements for the application.  See the [CPU](#cpu-attributes) section below.|
| memory | string |  N  | The minimum amount of memory required. The value is given in binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes). This is defined by the application developer. After deployment of the application, the device MUST provide this amount of memory for the application.|
| storage | string |  N  | The amount of storage required for the application to run. This encompasses the installed application and the data it needs to store. The value is given in binary units (`Ki` = Kibibytes, `Mi` = Mebibytes, `Gi` = Gibibytes, `Ti` Tebibytes, `Pi` = Pebibytes, `Ei` = Exbibytes). This is defined by the application developer. After deployment of the application, the device MUST provide this amount of storage for the application|
| peripherals | []Peripheral |  N  | Peripherals element specifying the peripherals required to run the application.  See the [Peripheral](#peripheral-attributes) section below.|
| interfaces | []CommunicationInterface |  N  | Interfaces element specifying the communication interfaces required to run the application.  See the [Communication Interfaces](#communicationinterface-attributes) section below.|


### CPU Attributes  <br><br>
CPU element specifying the CPU requirements for the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| cores | double |  Y  | The required amount of CPU cores the application must use to run in its full functionality. Specified as decimal units of CPU cores (e.g., `0.5` is half a core). This is defined by the application developer. After deployment of the application, the device MUST provide this number of CPU cores for the application.|
| architectures | []CpuArchitectureType |  N  | The CPU architectures supported by the application. This can be e.g. amd64, x86_64, arm64, arm. See the [CpuArchitectureType](#cpuarchitecturetype) definition for all permissible values. Multiple arcitecture types can be specified, as the deployment profile may support multiple CPU architectures.|


### Peripheral Attributes  <br><br>
Peripheral hardware of a device. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| type | PeripheralType |  Y  | The type of peripheral. This can be e.g. GPU, display, camera, microphone, speaker. See the [PeriperalType](#peripheraltype) definition for all permissible values.|
| manufacturer | string |  N  | The name of the manufacturer. If `manufacturer` is specified as a requirement here, it may be difficult to find devices that can host the  application. Please use these requirements with caution.|
| model | string |  N  | The model of the peripheral. If `model` is specified as a requirement here, it may be difficult to find devices that can host the application. Please use these requirements with caution.|


### CommunicationInterface Attributes  <br><br>
Communication interface of a device. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| type | CommunicationInterfaceType |  N  | The type of a communication interface. This can be e.g. Ethernet, WiFi, Cellular, Bluetooth, USB, CANBus, RS232. See the [CommunicationInterfaceType](#communicationinterfacetype) definition for all permissible values.|


### Component Attributes  <br><br>
A class representing a component of a deployment profile. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  Y  | A unique name used to identify the component package. For helm installations the name will be used as the chart name. The name must be lower case letters and numbers and MAY contain dashes.  Uppercase letters, underscores and periods MUST NOT be used.|
| properties | ComponentProperties |  Y  | A dictionary element specifying the component packages's deployment details.  See the [Component Properties](#componentproperties-attributes) section below.|


### ComponentProperties Attributes
The expected properties for the suppported deployment types are indicated below.

- Properties for `helm.v3` components

| Attribute      | Type  | Required?     | Description    |
| --- | --- | --- | --- |
| repository     | string |  Y  | The URL indicating the helm chart's location.|
| revision      | string |  Y  | The helm chart's full version.|
| wait | bool  | N  | If `True`, indicates the device MUST wait until the helm chart has finished installing before installing the next helm chart. The default is `True`. The Workload Fleet Management Client MUST support `True` and MAY support `False`. Only applies if multiple `helm.v3` components are provided.|
| timeout | string      | N   | The time to wait for the component's installation to complete. If the installation does not completed before the timeout occurs the installation process fails. The format is "##m##s" indicating the total number of minutes and seconds to wait. |  

- Properties for `compose` components

> **Investigation Needed**: We need to have more discussion about how Compose should be handled and what is required here.

| Attribute      | Type  | Required?     | Description    |
| --- | --- | --- | --- |
| packageLocation  | string |  Y  | The URL indicating the Compose package's location. |
| keyLocation    | string | N  | The public key used to validated the digitally signed package. It is highly recommend to digitally sign the package. When signing the package PGP MUST be used.|
| wait | bool  | N  | If `True`, indicates the device MUST wait until the Compose file has finished starting up before starting the next Compose file. The default is `True`. The Workload Fleet Management Client MUST support `True` and MAY support `False`. Only applies if multiple `compose` components are provided.|
| timeout | string      | N   | The time to wait for the component's installation to complete. If the installation does not completed before the timeout occurs the installation process fails. The format is "##m##s" indicating the total number of minutes and seconds to wait.|

## Defining configurable application parameters

To allow customizable configuration values when installing an application, the *application description*  defines the parameters and configuration sections giving the application vendor control over what can be configured when installing, or updating, an application. The [configuration](#configuration-attributes) section describes how the workload orchestration software vendor must display parameters to the user to allow them to specify the values. The [schema](#schema-attributes) section describes how the workload orchestration software vendor must validate the values provided by the user before the application is installed or updated.

> **Note:** At this point the specification only deals with parameter values provided by the user as part of installing, or updating, the application. We anticipate parameter values to come from other sources, such as the device, in the future and not only from the user.

### Parameter Attributes  <br><br>
Defines a configurable parameter for the application. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  Y  | Name of the parameter.|
| value | <*see description*> |  N  | The parameter's default value.  Accepted data types are string, integer, double, boolean, array[string], array[integer], array[double], array[boolean].|
| targets | []Target |  Y  | Used to indicate which component the value should be applied to when installing, or updating, the application.  See the [Target](#target-attributes) section below.|


### Target Attributes  <br><br>
Specifies where the parameter applies in the deployment. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| pointer | string |  Y  | The name of the parameter in the deployment configuration.  For Helm deployments, this is the dot notation for the matching element in the `values.yaml` file. This follows the same naming convention you would use with the `--set` command line argument with the `helm install` command.  For compose deployments, this is the name of the environment variable to set.|
| components | []string |  Y  | Indicates which deployment profile [component](#component-attributes the parameter target applies to.  The component name specified here MUST match a component name in the [deployment profiles](#deploymentprofile-attributes) section.|


### Configuration Attributes  <br><br>
Configuration layout and validation rules. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| sections | []Section |  Y  | Sections are used to group related parameters together,  so it is possible to present a user interface with a logical grouping of the parameters in each section.  See the [Section](#section-attributes) section below.|
| schema | []Schema |  Y  | Schema is used to provide details about how to validate each parameter value.  At a minimum, the parameter value must be validated to match the schema's data type.  The schema indicates additional rules the provided value must satisfy to be considered valid input.  See the [Schema](#schema-attributes) section below.|


### Section Attributes  <br><br>
Named sections within the configuration layout. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  Y  | The name of the section. This may be used in the user interface to show the grouping of the associated parameters within the section.|
| settings | []Setting |  Y  | Settings are used to provide instructions to the workload orchestration software vendor for displaying parameters to the user.  A user MUST be able to provide values for all settings.  See the [Setting](#setting-attributes) section below.|


### Setting Attributes  <br><br>
Individual configuration settings. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| parameter | string |  Y  | The name of the [parameter](#parameter-attributes) the setting is associated with.|
| name | string |  Y  | The parameter's display name to show in the user interface.|
| description | string |  N  | The parameters's short description to provide additional context to the user in the user interface about what the parameter is for.|
| immutable | boolean |  N  | If true, indicates the parameter value MUST not be changed once it has been set and used to install the application. Default is false if not provided.|
| schema | string |  Y  | The name of the schema definition to use to validate the parameter's value. See the [Schema](#schema-attributes) section below.|


### Schema Attributes  <br><br>
Defines data type and rules for validating user provided parameter values. Subclasses (see below) define for each data type their own set of validation rules that can be used. The value MUST be validated against all rules defined in the schema. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| name | string |  Y  | The name of the schema rule. This used in the [setting](#setting-attributes) to link the setting to the schema rule.|
| dataType | string |  Y  | Indicates the expected data type for the user provided value.  Accepted values are string, integer, double, boolean, array[string], array[integer], array[double], array[boolean].  At a minimum, the provided parameter value MUST match the schema's data type if no other validation rules are provided.|


* #### TextValidationSchema Attributes  <br>
(Subclass of Schema)  <br><br>
Extends schema to define a string/text-specific set of validation rules that can be used. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| allowEmpty | boolean |  N  | If true, indicates a value must be provided. Default is false if not provided.|
| minLength | integer |  N  | If set, indicates the minimum number of characters the value must have to be considered valid.|
| maxLength | integer |  N  | If set, indicates the maximum number of characters the value must have to be considered valid.|
| regexMatch | string |  N  | If set, indicates a regular expression to use to validate the value.|


* #### BooleanValidationSchema Attributes  <br>
(Subclass of Schema)  <br><br>
Extends schema to define a boolean-specific set of validation rules that can be used. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| allowEmpty | boolean |  N  | If true, indicates a value must be provided. Default is false if not provided.|


* #### NumericIntegerValidationSchema Attributes  <br>
(Subclass of Schema)  <br><br>
Extends schema to define a integer-specific set of validation rules that can be used. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| allowEmpty | boolean |  N  | If true, indicates a value must be provided. Default is false if not provided.|
| minValue | integer |  N  | If set, indicates the minimum allowed integer value the value must have to be considered valid.|
| maxValue | integer |  N  | If set, indicates the maximum allowed integer value the value must have to be considered valid.|


* #### NumericDoubleValidationSchema Attributes  <br>
(Subclass of Schema)  <br><br>
Extends schema to define a double-specific set of validation rules that can be used. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| allowEmpty | boolean |  N  | If true, indicates a value must be provided. Default is false if not provided.|
| minValue | float |  N  | If set, indicates the minimum value to be considered valid.|
| maxValue | float |  N  | If set, indicates the maximum value to be considered valid.|
| minPrecision | integer |  N  | If set, indicates the minimum level of precision the value must have to be considered valid.|
| maxPrecision | integer |  N  | If set, indicates the maximum level of precision the value must have to be considered valid.|


* #### SelectValidationSchema Attributes  <br>
(Subclass of Schema)  <br><br>
Extends schema to define a specific set of validation rules that can be used for select options. <br> 

| Attribute | Type | Required? | Description |
| --- | --- | --- | --- |
| allowEmpty | boolean |  N  | If true, indicates a value must be provided. Default is false if not provided.|
| multiselect | boolean |  N  | If true, indicates multiple values can be selected. If multiple values can be selected the resulting value is an array of the selected values. The default is false if not provided.|
| options | []string |  Y  | This provides the list of acceptable options the user can select from. The data type for each option must match the parameter setting’s data type.|



## Enumerations
These enumerations are used as vocabularies for attribute values of the `ApplicationDescription`.

### CpuArchitectureType

| Permissible Values | Description |
| --- | --- |
| amd64 | AMD 64-bit architecture.|
| x86_64 | x86 64-bit architecture.|
| arm64 | ARM 64-bit architecture.|
| arm | ARM 32-bit architecture. |  

### CommunicationInterfaceType

| Permissible Values | Description |
| --- | --- |
| ethernet | This type stands for an Ethernet interface.|
| wifi | This type stands for an WiFi interface.|
| cellular | This type stands for cellular communication technologies such as 5G, LTE, 3G, 2G, ....|
| bluetooth | This type stands for a Bluetooth or Bluetooth Low-Energy (BLE) interface. |  
| usb | This type stands for a USB interface.|
| canbus | This type stands for a CANBus interface.|
| rs232 | This type stands for a RS232 interface. |  

### PeripheralType

| Permissible Values | Description |
| --- | --- |
| gpu | This type stands for a Graphics Processing Unit (GPU) peripheral.|
| display | This type stands for a display peripheral.|
| camera | This type stands for a camera peripheral.|
| microphone | This type stands for a microphone peripheral. |
| speaker | This type stands for a speaker peripheral. |



## Application Description Examples

### Example 1: Simple Application Description
A simple hello-world example of an `ApplicationDescription` is shown below:

```yaml
apiVersion: margo.org/v1-alpha1
kind: ApplicationDescription
metadata:
  id: com-northstartida-hello-world
  name: Hello World
  description: A basic hello world application
  version: "1.0"
  catalog:
    application:
      icon: ./resources/hw-logo.png
      tagline: Northstar Industrial Application's hello world application.
      descriptionFile: ./resources/description.md
      releaseNotes: ./resources/release-notes.md
      licenseFile: ./resources/license.pdf
      site: http://www.northstar-ida.com
      tags: ["monitoring"]
    author:
      - name: Roger Wilkershank
        email: rpwilkershank@northstar-ida.com
    organization:
      - name: Northstar Industrial Applications
        site: http://northstar-ida.com
deploymentProfiles:
  - type: helm.v3
    id: com-northstartida-hello-world-helm.v3-a
    components:
      - name: hello-world
        properties:  
          repository: oci://northstarida.azurecr.io/charts/hello-world
          revision: 1.0.1
          wait: true
parameters:
  greeting:
    value: Hello
    targets:
    - pointer: global.config.appGreeting
      components: ["hello-world"]
  greetingAddressee:
    value: World
    targets:
    - pointer: global.config.appGreetingAddressee
      components: ["hello-world"]
configuration:
  sections:
    - name: General Settings
      settings:
        - parameter: greeting
          name: Greeting
          description: The greeting to use.
          schema: requireText
        - parameter: greetingAddressee
          name: Greeting Addressee
          description: The person, or group, the greeting addresses.
          schema: requireText
  schema:
    - name: requireText
      dataType: string
      maxLength: 45
      allowEmpty: false
```

### Example 2: Application Description with Deployment Profiles for Helm and Compose
An example of an `ApplicationDescription` defining [deployment profiles](#deploymentprofile-attributes) for both cases, Helm chart as well as Compose, is shown below.

```yaml
apiVersion: margo.org/v1-alpha1
kind: ApplicationDescription
metadata:
  id: com-northstartida-digitron-orchestrator
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
      tags: ["optimization", "instrumentation"]
    author:
      - name: Roger Wilkershank
        email: rpwilkershank@northstar-ida.com
    organization:
      - name: Northstar Industrial Applications
        site: http://northstar-ida.com
deploymentProfiles:
  - type: helm.v3
    id: com-northstartida-digitron-orchestrator-helm.v3-a
    description: This allows to install / run the application as a Helm chart deployment.
      The device where this application is installed needs to have a screen and a keyboard (as indicated in the required peripherals).
    components:
      - name: database-services
        properties: 
          repository: oci://quay.io/charts/realtime-database-services
          revision: 2.3.7
          wait: true
          timeout: 8m30s
      - name: digitron-orchestrator
        properties:
          repository: oci://northstarida.azurecr.io/charts/northstarida-digitron-orchestrator
          revision: 1.0.9
          wait: true
    requiredResources:
      cpu: 
        cores: 1.5
        architectures: 
          - amd64 
          - x86_64
      memory: 1024Mi
      storage: 10Gi
      peripherals:
        - type: gpu
          manufacturer: NVIDIA
        - type: display
      interfaces:
        - type: ethernet
        - type: bluetooth
  - type: compose
    id: com-northstartida-digitron-orchestrator-compose-a
    components:
      - name: digitron-orchestrator-docker
        properties:
          packageLocation: https://northsitarida.com/digitron/docker/digitron-orchestrator.tar.gz
          keyLocation: https://northsitarida.com/digitron/docker/public-key.asc
parameters:
  idpName:
    targets:
      - pointer: idp.name
        components: ["digitron-orchestrator"]
      - pointer: ENV.IDP_NAME
        components: ["digitron-orchestrator-docker"]
  idpProvider:
    targets:
      - pointer: idp.provider
        components: ["digitron-orchestrator"]
      - pointer: ENV.IDP_PROVIDER
        components: ["digitron-orchestrator-docker"]
  idpClientId:
    targets:
      - pointer: idp.clientId
        components: ["digitron-orchestrator"]
      - pointer: ENV.IDP_CLIENT_ID
        components: ["digitron-orchestrator-docker"]
  idpUrl:
    targets:
      - pointer: idp.providerUrl
        components: ["digitron-orchestrator"]
      - pointer: idp.providerMetadata
        components: ["digitron-orchestrator"]
      - pointer: ENV.IDP_URL
        components: ["digitron-orchestrator-docker"]
  adminName:
    targets:
      - pointer: administrator.name
        components: ["digitron-orchestrator"]
      - pointer: ENV.ADMIN_NAME
        components: ["digitron-orchestrator-docker"]
  adminPrincipalName:
    targets:
      - pointer: administrator.userPrincipalName
        components: ["digitron-orchestrator"]
      - pointer: ENV.ADMIN_PRINCIPALNAME
        components: ["digitron-orchestrator-docker"]
  pollFrequency:
    value: 30
    targets: 
      - pointer: settings.pollFrequency
        components: ["digitron-orchestrator", "database-services"]
      - pointer: ENV.POLL_FREQUENCY
        components: ["digitron-orchestrator-docker"]
  siteId:
    targets:
      - pointer: settings.siteId
        components: ["digitron-orchestrator", "database-services"]
      - pointer: ENV.SITE_ID
        components: ["digitron-orchestrator-docker"]
  cpuLimit:
    value: 1 
    targets:
      - pointer: settings.limits.cpu
        components: ["digitron-orchestrator"]
  memoryLimit:
    value: 16384
    targets:
      - pointer: settings.limits.memory
        components: ["digitron-orchestrator"]
configuration:
  sections:
    - name: General
      settings:
        - parameter: pollFrequency
          name: Poll Frequency
          description: How often the service polls for updated data in seconds
          schema: pollRange
        - parameter: siteId
          name: Site Id
          description: Special identifier for the site (optional)
          schema: optionalText
    - name: Identity Provider
      settings:
        - parameter: idpName
          name: Name
          description: The name of the Identity Provider to use
          immutable: true
          schema: requiredText
        - parameter: idpProvider
          name: Provider
          description: Provider something something
          immutable: true
          schema: requiredText
        - parameter: idpClientId
          name: Client ID
          description: The client id
          immutable: true
          schema: requiredText
        - parameter: idpUrl
          name: Provider URL
          description: The url of the Identity Provider
          immutable: true
          schema: url
    - name: Administrator
      settings:
        - parameter: adminName
          name: Presentation Name
          description: The presentation name of the administrator
          schema: requiredText
        - parameter: adminPrincipalName
          name: Principal Name
          description: The principal name of the administrator
          schema: email
    - name: Resource Limits
      settings:
        - parameter: cpuLimit
          name: CPU Limit
          description: Maximum number of CPU cores to allow the application to consume
          schema: cpuRange
        - parameter: memoryLimit
          name: Memory Limit
          description: Maximum number of memory to allow the application to consume
          schema: memoryRange
  schema:
    - name: requiredText
      dataType: string
      maxLength: 45
      allowEmpty: false
    - name: email
      dataType: string
      allowEmpty: false
      regexMatch: .*@[a-z0-9.-]*
    - name: url
      dataType: string
      allowEmpty: false
      regexMatch: ^(http(s):\/\/.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$
    - name: pollRange
      dataType: integer
      minValue: 30
      maxValue: 360
      allowEmpty: false
    - name: optionalText
      dataType: string  
      minLength: 5
      allowEmpty: true
    - name: cpuRange
      dataType: double
      minValue: 0.5
      maxPrecision: 1
      allowEmpty: false
    - name: memoryRange
      dataType: integer
      minValue: 16384
      allowEmpty: false
```