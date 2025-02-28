# Envisioned System Design

Margo intends to create an open [interoperability](./technical-lexicon.md#interoperability) standard and ecosystem for the industrial edge, allowing [edge compute devices](./technical-lexicon.md#edge-compute-device), [workloads](./technical-lexicon.md#workload), and [fleet management](./technical-lexicon.md#fleet-management-concepts) software to be compatible and interoperable across manufacturers and software developers willing to adopt such standard.

## Overview

![System Design Drawing)](../figures/System-design.drawio.svg)

The envisioned system can be broken down into the following main components:

### Workloads

Workloads are the software deployed to Margo-compliant edge compute devices. See the [workloads overview](./application-package-overview.md) page to learn more Margo's supported workloads and how the are packaged.

### Workload Observability

For distributed systems its vitally important to collect diagnostics information about the workloads and systems running within the environment. See the [workload observability overview](./workload-observability-overview.md) page to see how Margo is making use of the Open Telemetry specification to capture this information.

### Workload Fleet Management

Workload fleet management software is the centralized software solution for managing the lifecycle of workloads on Margo compliant edge compute devices. See the [workload fleet management](./workload-management-interface-overview.md) page to learn more more.  

### Edge compute devices

Edge compute devices are the compute surfaces workloads are deployed to and run on. As part of the Margo initiative we are very prescriptive about how a edge compute devices must be configured to make it Margo compliant. See the [edge compute device overview](./devices-overview.md) page to learn more.


