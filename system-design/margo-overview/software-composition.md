# Software Composition

Applications can be found in completely different stages:

1. "Application Packaging": application has been prepared and made ready for staging.
2. "Application Staging": application is set up, configured, and made available for use to the device, but has not yet been deployed (started) to be used.
3. "Application Deployment" (AKA Runtime): application has been made available and accessible on the device.

Distinguishing which stage terminology refers to is important to understand the scope of following definitions.

## Terminology Scoping

#### Application

The term [application](technical-lexicon.md#application) refers to all three stages.

#### Workload

The term [workload](technical-lexicon.md#workload) applies only to [running software](#3-software-deployment).

The term [component](#component) applies to the resources available in [packaged software](#1-software-packaging) and [staged software](#2-software-staging) for the workload to run.

#### Component

The term [component](#component) applies to the resources available in [packaged software](#1-software-packaging) and [staged software](#2-software-staging) for the workload to run.

The instantiation of a component results in a [workload](#workload).

Components might have different shapes depending on the workload type and on which stage is being considered:

1. Helm v3 as Packaged Software: a [Helm Chart](https://helm.sh/docs/topics/charts/)
2. Helm v3 as Staged software: all container images required by the to-be-started pods.
3. Compose as Packaged Software: a [Compose Archive](../app-interoperability/application-package-definition.md)
4. Compose as Staged software: a so-called [Compose file](https://github.com/compose-spec/compose-spec/blob/main/spec.md#compose-file) and all the container images required by the to-be-started [services](https://github.com/compose-spec/compose-spec/blob/main/05-services.md).

## Stages

### 1. Software Packaging

```mermaid
C4Context
    title Software Packaging stage

    Enterprise_Boundary(be, "Backend") {
        System(app, "ApplicationDescription", "Application Package")
    }
    UpdateElementStyle(app, $fontColor="white", $bgColor="blue", $borderColor="grey")
```

Software at rest requires following resources:

- an application definition: a Margo-specific way to distribute a composition of one or more components
- some application resources: icon, license(s), release notes,...
- some components: a well-specified way to distribute software supported by Margo specification (e.g. Helm Chart and container images, Compose Archive,...)

They are managed and hosted separately:

- application registries store application definitions and their associated application resources 
- component registries store components

⁉️ _QUESTION_: what is an application catalog? are there component catalogs? what's that?

The following diagram shows the mentioned registries and resources (container images are not shown for simplicity):

```mermaid
C4Component
    title Application Bundling: applications-workload definitions relationship

    System_Boundary(ar, "Application Registry") {
        Container_Boundary(ab2, "Application Package 2") {
            Component(atb2, "Application Description 2", "ApplicationDescription", "YAML document")
            Component(o2, "...", "Others")
        }

        Container_Boundary(ab1, "Application Package 1") {
            Component(atb1, "Application Description 1", "ApplicationDescription", "YAML document")
            Component(o1, "...", "Others")
        }
        
        Container_Boundary(ab4, "Application Package 4") {
            Component(atb4, "Application Description 4", "ApplicationDescription", "YAML document")
            Component(o4, "...", "Others")
        }

        Container_Boundary(ab3, "Application Package 3") {
            Component(atb3, "Application Description 3", "ApplicationDescription", "YAML document")
            Component(o3, "...", "Others")
        }
    }

    System_Boundary(crr, "Component Registry") {
        Component(hc1, "Helm Chart 1", "Component")
        Component(hc2, "Helm Chart 2", "Component")
        Component(hc3, "Helm Chart 3", "Component")
        Component(cc1, "Compose Archive 1", "Component", "TARball")
        Component(cc2, "Compose Archive 2", "Component", "TARball")
    }

    Rel(atb1, hc1, "refers")
    Rel(atb1, hc2, "refers")
    Rel(atb1, cc1, "refers")

    Rel(atb2, hc1, "refers")
    Rel(atb1, hc3, "refers")

    Rel(atb3, hc3, "refers")
    Rel(atb3, cc1, "refers")

    Rel(atb4, cc2, "refers")

    UpdateElementStyle(atb1, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(atb2, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(atb3, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(atb4, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(hc1, $fontColor="black", $bgColor="khaki", $borderColor="grey")
    UpdateElementStyle(hc2, $fontColor="black", $bgColor="khaki", $borderColor="grey")
    UpdateElementStyle(hc3, $fontColor="black", $bgColor="khaki", $borderColor="grey")
    UpdateElementStyle(cc1, $fontColor="black", $bgColor="lightsalmon", $borderColor="grey")
    UpdateElementStyle(cc2, $fontColor="black", $bgColor="lightsalmon", $borderColor="grey")
```

The following diagram shows the relationship between the different resources of an application bundle and the required components for an example application providing both Helm v3 and Compose deployment profiles:

```mermaid
C4Component
    title Application Bundling: Example 1 - Helm and Compose deployment profiles provided

    System_Boundary(ar, "Application Registry") {
        Container_Boundary(ab1, "Application Package 1") {
            Component(atb1, "Application Package", "Reference", "Git reference? OCI manifest?")

            Container_Boundary(c99, "Resources") {
                Component(rd, "Resources", "Directory")
                Component(ic, "Icon", "File(s)")
                Component(lc, "License", "File(s)")
                Component(rn, "Release Notes", "File(s)")
                Rel(rd, ic, "contains")
                Rel(rd, lc, "contains")
                Rel(rd, rn, "contains")
            }

            Container_Boundary(c1, "Application Description") {
                Component(ad, "Application Description", "ApplicationDescription", "YAML document")
                Container_Boundary(c2, "deploymentProfiles") {
                    Container_Boundary(c3, "helm.v3") {
                        Component(wldh1, "Helm WorkloadArtifact 1", "Section in YAML document")
                    }
                    Container_Boundary(c4, "compose") {
                        Component(wldc1, "Compose WorkloadArtifact 1", "Section in YAML document")
                    }
                }
                Rel(ad,wldh1, "defines")
                Rel(ad,wldc1, "defines")
            }

            Rel(atb1, ad, "requires")
            Rel(atb1, rd, "requires")
        }
    }

    System_Boundary(crr, "Component Registry") {
        Component(hc1, "Helm Chart 1", "Component")
        Component(cc1, "Compose Archive 1", "Component", "TARball")
    }

    Rel(wldh1, hc1, "refers")
    Rel(wldc1, cc1, "refers")

    UpdateElementStyle(ad, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(hc1, $fontColor="black", $bgColor="khaki", $borderColor="grey")
    UpdateElementStyle(cc1, $fontColor="black", $bgColor="lightsalmon", $borderColor="grey")
```

The following diagram shows the top-level structure of a Compose component:

```mermaid
C4Component
    title Application Bundling: Example 2 - focus on Worload Definition registry

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="3")

    System_Boundary(ar, "Application Registry") {
        Container_Boundary(ab1, "Application Package 1") {
            Component(atb1, "Application Package", "Git reference? OCI manifest?")

            Container_Boundary(c1, "Application Description") {
                Component(ad, "Application Description", "YAML document")
                Container_Boundary(c2, "deploymentProfiles") {
                    Container_Boundary(c4, "compose") {
                        Component(wldc1, "Compose WorkloadArtifact 1")
                    }
                }
                Rel(ad,wldc1, "defines")
            }

            Component(rd, "Resources", "Directory")

            Rel(atb1, ad, "requires")
            Rel(atb1, rd, "requires")
        }
    }

    System_Boundary(crr, "Component Registry") {
        Component(cc1, "Compose Configuration 1", "Compose")
        Component(ca1, "Compose Archive 1", "Component", "TARball")
        Rel(ca1, cc1, "contains")
        UpdateRelStyle(cc1, cim1, $offsetY="50")
    }

    System_Boundary(cir, "Container Image Registry") {
        Component(cim1, "Container Image 1", "Archive")
    }

    Rel(wldc1, ca1, "refers")
    Rel(cc1, cim1, "refers")

    UpdateElementStyle(ad, $fontColor="white", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(ca1, $fontColor="black", $bgColor="lightsalmon", $borderColor="grey")
```

The application and contained components are typically configurable with the option of providing default values.

### 2. Software Staging

⁉️ _QUESTION_: what is the connection between `ApplicationDescription` and `ApplicationDeployment`?

ℹ️ _NOTE_: stage completely out of scope as of now.

⁉️ _QUESTION_: How to get an application staged, but not deployed?

```mermaid
C4Context
    title Software Staging stage

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="2")

    Enterprise_Boundary(be, "Backend") {
        System(apdb, "ApplicationDeployment", "Application Deployment specification")
        System(appb, "ApplicationDescription", "Application Package")
    }

    Enterprise_Boundary(dev, "Device") {
        System(apdd, "ApplicationDeployment", "Application Deployment specification")
        System(wls, "Components")
        System(appd, "ApplicationDescription", "Application Package")
        Rel(apdd, wls, "requires")
    }

    BiRel(apdb, apdd, "same")
    BiRel(appb, appd, "same")
    UpdateElementStyle(appb, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(appd, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(apdb, $fontColor="black", $bgColor="green", $borderColor="grey")
    UpdateElementStyle(apdd, $fontColor="black", $bgColor="green", $borderColor="grey")
```

When a device gets the instruction to stage an application (indirectly over a desired-state specified with an [`ApplicationDeployment` object](https://specification.margo.org/margo-api-reference/workload-api/desired-state-api/desired-state/?h=applicationdeployment#applicationdeployment-definition)), its Workload Fleet Management Agent interacts with the [providers](https://specification.margo.org/margo-overview/technical-lexicon/#provider-model) (e.g. Helm client) to stage the components.

In this stage the [providers](https://specification.margo.org/margo-overview/technical-lexicon/#provider-model) are responsible for managing the components.

On a Helm v3 deployment profile, the Workload Fleet Management Agent will instruct the Helm API to install the specified Helm Charts.

On a Compose deployment profile, the Workload Fleet Management Agent will instruct the corresponding middleware (remember that Compose components are archives containing Compose configurations and other resources) to install the component.

Following diagram shows the result of staging an application and the corresponding components on a Helm v3 deployment profile (the result of `helm pull`).

```mermaid
C4Component
    title Application Staging: Helm v3 deployment profile

    UpdateLayoutConfig($c4BoundaryInRow="3", $c4ShapeInRow="1")

    System_Boundary(dev1, "Device 1") {
        System_Boundary(woa1, "Workload Fleet Management Agent") {
            Component(atb1, "ApplicationDeployment 1", "ApplicationDeployment", "YAML document")
        }

        System_Boundary(hel1, "Helm") {
            Component(hc1, "Helm Chart File 1", "YAML file")
            Component(hc2, "Helm Chart File 2", "YAML file")
        }

        System_Boundary(fs1, "File System") {
            System_Boundary(doc1, "Docker Engine") {
                Component(cim1, "Container Image 1")
                Component(cim2, "Container Image 2")
                Component(cim3, "Container Image 3")
            }
        }
    }

    Rel(atb1, hc1, "refers")
    Rel(hc1, cim1, "refers")
    Rel(atb1, hc2, "refers")
    Rel(hc2, cim1, "refers")
    Rel(hc2, cim2, "refers")
    Rel(hc2, cim3, "refers")

    UpdateElementStyle(atb1, $fontColor="white", $bgColor="blue", $borderColor="grey")
```

The following diagram shows the result of staging an application and the corresponding components on a Compose deployment profile (the result of `compose pull`).

```mermaid
C4Component
    title Application Staging: Compose deployment profile

    UpdateLayoutConfig($c4BoundaryInRow="3", $c4ShapeInRow="1")

    System_Boundary(dev1, "Device 1") {
        System_Boundary(woa1, "Workload Fleet Management Agent") {
            Component(atb1, "ApplicationDeployment 1", "ApplicationDeployment", "YAML document")
        }

        System_Boundary(fs1, "File System") {
            Component(cc1, "Compose Configuration 1")
            Component(cc2, "Compose Configuration 2")
            System_Boundary(doc1, "Docker Engine") {
                Component(cim1, "Container Image 1")
                Component(cim2, "Container Image 2")
                Component(cim3, "Container Image 3")
            }
        }
    }

    Rel(atb1, cc1, "refers")
    Rel(atb1, cc2, "refers")
    Rel(cc1, cim1, "refers")
    Rel(cc2, cim2, "refers")
    Rel(cc2, cim3, "refers")

    UpdateElementStyle(atb1, $fontColor="white", $bgColor="green", $borderColor="grey")
```

### 3. Software Deployment

```mermaid
C4Context
    title Software Deployment stage

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="2")

    Enterprise_Boundary(be, "Backend") {
        System(apdb, "ApplicationDeployment", "Application Deployment specification")
        System(appb, "ApplicationDescription", "Application Package")
    }

    Enterprise_Boundary(dev, "Device") {
        System(apdd, "ApplicationDeployment", "Application Deployment specification")
        System(wls, "Workload")
        System(appd, "ApplicationDescription", "Application Package")
        Rel(apdd, wls, "configures")
    }

    BiRel(apdb, apdd, "same")
    BiRel(appb, appd, "same")
    UpdateElementStyle(appb, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(appd, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(apdb, $fontColor="black", $bgColor="green", $borderColor="grey")
    UpdateElementStyle(apdd, $fontColor="black", $bgColor="green", $borderColor="grey")
```

When a device gets the instruction to run an application (over a desired-state specified with an [`ApplicationDeployment` object](https://specification.margo.org/margo-api-reference/workload-api/desired-state-api/desired-state/?h=applicationdeployment#applicationdeployment-definition)), its Workload Fleet Management Agent interacts with the [providers](https://specification.margo.org/margo-overview/technical-lexicon/#provider-model).
That way all workloads needed for an application should get started and the desired state should be reached.

In this stage the [providers](https://specification.margo.org/margo-overview/technical-lexicon/#provider-model) are responsible for managing the individual workloads.

On a Helm v3 deployment profile, the Workload Fleet Management Agent will instruct the Helm API to start the individual Helm Charts.

On a Compose deployment profile, the Workload Fleet Management Agent will instruct the Compose CLI to start the individual workloads.

The following diagram shows the result of reaching the desired state for an application with a Helm v3 deployment profile (the result of `helm install`).

```mermaid
C4Component
    title Application Deployment: Helm v3 deployment profile

    UpdateLayoutConfig($c4BoundaryInRow="3", $c4ShapeInRow="1")

    System_Boundary(dev1, "Device 1") {
        System_Boundary(woa1, "Workload Fleet Management Agent") {
            Component(atb1, "Application Description 1", "ApplicationDescription", "YAML document")
        }

        System_Boundary(hel1, "Helm") {
            Component(hc1, "Helm Chart 1")
            Component(hc2, "Helm Chart 2")
        }

        System_Boundary(kbl1, "Kubelet") {
            Component(pod1, "Pod 1")
            Component(pod2, "Pod 2")
            Component(pod3, "Pod 3")
        }
    }

    Rel(atb1, hc1, "refers")
    Rel(hc1, pod1, "refers")
    Rel(atb1, hc2, "refers")
    Rel(hc2, pod2, "refers")
    Rel(hc2, pod3, "refers")
    Rel(hc2, pod3, "refers")

    UpdateElementStyle(atb1, $fontColor="white", $bgColor="blue", $borderColor="grey")
```

The following diagram shows the result of deploying an application and the corresponding components with a Compose deployment profile (the result of `compose up`).

```mermaid
C4Component
    title Application Deployment: Compose deployment profile

    UpdateLayoutConfig($c4BoundaryInRow="3", $c4ShapeInRow="1")

    System_Boundary(dev1, "Device 1") {
        System_Boundary(woa1, "Workload Fleet Management Agent") {
            Component(atb1, "Application Description 1", "ApplicationDescription", "YAML document")
        }

        System_Boundary(fs1, "File System") {
            Component(cc1, "Compose Configuration 1")
            Component(cc2, "Compose Configuration 2")
            System_Boundary(doc1, "Docker Engine") {
                Component(srv1, "Service 1")
                Component(srv2, "Service 2")
                Component(srv3, "Service 3")
            }
        }
    }

    Rel(atb1, cc1, "refers")
    Rel(atb1, cc2, "refers")
    Rel(cc1, srv1, "refers")
    Rel(cc2, srv2, "refers")
    Rel(cc2, srv3, "refers")

    UpdateElementStyle(atb1, $fontColor="white", $bgColor="blue", $borderColor="grey")
```
