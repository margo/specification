# Software Composition

[Applications][application] can be found in completely different stages:

1. "Application Packaging": application has been prepared and made ready for deployment.
2. "Application Deployment" (AKA Runtime): application has been made available and accessible on the device.

Distinguishing which stage terminology refers to is important to understand the scope of following definitions.

ℹ️ _Note_: Logically there is another intermediate stage: "Application Staging". This is the stage in which the application is set up, configured, and made available for use to the device, but has not yet been deployed (started) to be used. As of now this stage is out of scope in the Margo specification and not being considered, because some of the providers (like the Helm one) do not provide any mechanisms to manage it.

## Terminology Scoping

This section does not declare terminology, that is the task of the [Technical Lexicon](technical-lexicon.md), but rather tries to scope some of the terms to the above mentioned stages.

#### Application

The term [application][application] applies to all stages.

#### Workload

The term [Workload][workload] applies only to [running software](#2-software-deployment).

[Workloads][workload] are the result of deploying [Components][component].

#### Component

The term [Component][component] applies to the resources available in [packaged software](#1-software-packaging) that get instantiated into [Workloads][workload].

Some providers might support that multiple [Workload][workload] replicas are instantiated from a single [Component][component].

[Components][component] are made available over [Component Catalogs][component-catalog].

[Components][component] might have different shapes depending on their type and on which stage is being considered:

1. Helm v3 as [Component][component]: a [Helm Chart](https://helm.sh/docs/topics/charts/)
2. Helm v3 as [Workload][workload]: all container images required by the to-be-started pods.
3. Compose as [Component][component]: a [Compose Archive][compose-archive]
4. Compose as [Workload][workload]: a so-called [Compose file](https://github.com/compose-spec/compose-spec/blob/main/spec.md#compose-file) and all the container images required by the to-be-started [services](https://github.com/compose-spec/compose-spec/blob/main/05-services.md).

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

- an [Application Description][application-description]: a Margo-specific way to distribute a composition of one or more [Component][component]
- some application resources: icon, license(s), release notes,...
- some [Component][component]: a well-specified way to distribute software supported by Margo specification (e.g. Helm Chart and container images, Compose Archive,...)

[Application Descriptions][application-description], resources and [Components][component] are managed and hosted separately:

- [Application Registries][application-registry] store [Application Descriptions][application-description] and their associated application resources (as of now application registries SHALL be git repositories) 
- [Component Registries][component-registry] store components

The following diagram shows the mentioned registries and resources (container images are not shown for simplicity):

```mermaid
C4Component
    title Application Bundling: applications-workload definitions relationship

    System_Boundary(ar, "Application Registry (Git)") {
        System_Boundary(ab2, "Application Package 1") {
            Component(atb2, "Application Description 1", "ApplicationDescription", "YAML document")
            Component(o2, "...", "Others")
        }

        System_Boundary(ab1, "Application Package 2") {
            Component(atb1, "Application Description 2", "ApplicationDescription", "YAML document")
            Component(o1, "...", "Others")
        }
        
        System_Boundary(ab4, "Application Package 3") {
            Component(atb4, "Application Description 3", "ApplicationDescription", "YAML document")
            Component(o4, "...", "Others")
        }

        System_Boundary(ab3, "Application Package 4") {
            Component(atb3, "Application Description 4", "ApplicationDescription", "YAML document")
            Component(o3, "...", "Others")
        }
    }

    System_Boundary(crr, "Component Catalog") {
        Component(hc1, "Helm Chart 1", "Component")
        Component(hc2, "Helm Chart 2", "Component")
        Component(hc3, "Helm Chart 3", "Component")
        Component(cc1, "Compose Archive 1", "Component", "TARball")
        Component(cc2, "Compose Archive 2", "Component", "TARball")
    }

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

The following diagram shows the relationship between the different resources of an [Application][application] bundle and the required [Components][component] for an example application providing both Helm v3 and Compose [Deployment Profiles][deployment-profile]:

```mermaid
C4Component
    title Application Bundling: Example 1 - Helm and Compose deployment profiles provided

    System_Boundary(ar, "Application Registry (Git)") {
        System_Boundary(ab1, "Application Package 1") {
            Component(atb1, "Application Package", "Reference", "Git reference? OCI manifest?")

            System_Boundary(c99, "Resources") {
                Component(rd, "Resources", "Directory")
                Component(ic, "Icon", "File(s)")
                Component(lc, "License", "File(s)")
                Component(rn, "Release Notes", "File(s)")
                Rel(rd, ic, "contains")
                Rel(rd, lc, "contains")
                Rel(rd, rn, "contains")
            }

            System_Boundary(c1, "Application Description") {
                Component(ad, "Application Description", "ApplicationDescription", "YAML document")
                System_Boundary(c2, "deploymentProfiles") {
                    System_Boundary(c3, "helm.v3") {
                        Component(wldh1, "Helm WorkloadArtifact 1", "Section in YAML document")
                    }
                    System_Boundary(c4, "compose") {
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

    System_Boundary(crr, "Component Catalog") {
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
    title Application Bundling: Example 2 - focus on Component Catalog

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="3")

    System_Boundary(ar, "Application Registry (Git)") {
        System_Boundary(ab1, "Application Package 1") {
            Component(atb1, "Application Package", "Git reference? OCI manifest?")

            System_Boundary(c1, "Application Description") {
                Component(ad, "Application Description", "YAML document")
                System_Boundary(c2, "deploymentProfiles") {
                    System_Boundary(c4, "compose") {
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

    System_Boundary(crr, "Component Catalog") {
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

### 2. Software Deployment

```mermaid
C4Context
    title Software Deployment stage

    UpdateLayoutConfig($c4BoundaryInRow="1", $c4ShapeInRow="2")

    Enterprise_Boundary(be, "Backend") {
        System(apdb, "ApplicationDeployment", "Application Deployment specification")
        System(appb, "ApplicationDescription", "Application Package")
        System(cmp, "Component")
        Rel(appb, apdb, "deployment")
        Rel(appb, cmp, "requires")
    }

    Enterprise_Boundary(dev, "Device") {
        System(apdd, "ApplicationDeployment", "Application Deployment specification")
        System(wls, "Workload")
        Rel(apdd, wls, "configures")
    }

    BiRel(apdb, apdd, "same")
    Rel(cmp, wls, "instantiation")
    UpdateElementStyle(appb, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(appd, $fontColor="black", $bgColor="blue", $borderColor="grey")
    UpdateElementStyle(apdb, $fontColor="black", $bgColor="green", $borderColor="grey")
    UpdateElementStyle(apdd, $fontColor="black", $bgColor="green", $borderColor="grey")
```

When a device gets the instruction to run an [Application][application] (over a desired-state specified with an [`ApplicationDeployment` object][deployment-definition]), its [Workload Fleet Management Agent][wfma] interacts with the [providers][provider-model].
That way all [Workloads][workload] needed for an [Application][application] should get started and the desired state should be reached.

In this stage the [providers][provider-model] are responsible for managing the individual [Workloads][workload].

On a Helm v3 [Deployment Profiles][deployment-profile], the [Workload Fleet Management Agent][wfma] would probably instruct the Helm API to start the individual Helm Charts.

On a Compose [Deployment Profiles][deployment-profile], the [Workload Fleet Management Agent][wfma] would probably instruct the Compose CLI to start the individual [Workloads][workload].

The following diagram shows the result of reaching the desired state for an [Application][application] with a Helm v3 [Deployment Profiles][deployment-profile] (the result of `helm install`).

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

The following diagram shows the result of deploying an [Application][application] and the corresponding [Components][component] with a Compose [Deployment Profiles][deployment-profile] (the result of `compose up`).

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
            System_Boundary(doc1, "Container Engine") {
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

[application-description]: ../margo-api-reference/workload-api/application-package-api/application-description.md
[compose-archive]: ../app-interoperability/application-package-definition.md
[application-registry]: technical-lexicon.md#application-registry
[component]: technical-lexicon.md#component
[workload]: technical-lexicon.md#workload
[application]: technical-lexicon.md#application
[component-catalog]: technical-lexicon.md#component-catalog
[deployment-definition]: ../margo-api-reference/workload-api/desired-state-api/desired-state/?h=applicationdeployment.md#applicationdeployment-definition
[provider-model]: technical-lexicon.md/#provider-model
[wfma]: technical-lexicon/#workload-fleet-management-agent
[deployment-profile]: margo-api-reference/workload-api/application-package-api/application-description.md/#deploymentprofile-attributes
