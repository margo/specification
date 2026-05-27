# Publishing Workload Observability Data

Compliant workloads MAY choose to expose workload specific observability data by sending their observability data to the Open Telemetry collector on the standalone device or cluster. While this is optional, it is highly recommended in order to support distributed diagnostics.

Workload suppliers choosing to expose metrics, traces or logs for consumption with OpenTelemetry MUST send the data to the OpenTelemetry collector using OTLP.

The information required to communicate with the device's OTEL Collector is injected into each container using [environment variables](../observability/collecting-workload-observability-data.md#connecting-to-the-opentelemetry-collector).

Workload suppliers SHOULD NOT expect their workloads to be auto-instrumented by anything outside of their control (by the [OpenTelemetry operator](https://github.com/open-telemetry/opentelemetry-operator#opentelemetry-auto-instrumentation-injection) for example).

A workload supplier MAY choose an observability framework other than OpenTelemetry but it MUST be self-contained within the deployment of their workload. If an alternative approach is taken, it is NOT recommended workload suppliers publish their observability data outside the device/cluster by using any other means other than the Open Telemetry collector. If the workload supplier chooses to export data without using the OpenTelemetry collector they MUST NOT do this without the end user's approval.

> **Note:** See the [workload observability overview](../../overview/workload-observability.md) page for more information about workload observablity.
>
> **Action:** We may need to address in some form legacy workloads that are not currently using open telemetry and don't want to migrate their workload to use it.
