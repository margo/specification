Compliant applications MAY choose to expose application specific observability data by sending their observability data to the Open Telemetry collector on the standalone device or cluster. While this is optional, is it highly recommended in order to support distributed diagnostics.

Application developers choosing to expose application metrics, traces or logs for consumption with OpenTelemetry MUST send the data to the OpenTelemetry collector using OTLP.

The information required to communicate with the device's OTEL Collector is injected into each container using [environment variables](../device-interoperability/collecting-application-observability-data.md#connecting-to-the-opentelemetry-collector).

Application developers SHOULD NOT expect their applications to be auto-instrumented by anything outside of their control (by the [OpenTelemetry operator](https://github.com/open-telemetry/opentelemetry-operator#opentelemetry-auto-instrumentation-injection) for example).

An application developer MAY choose an observability framework other than OpenTelemetry but it MUST be self-contained within the deployment of their application. If an alternative approach is taken, it is NOT recommended application developers publish their observability data outside the device/cluster by using any other means other than the Open Telemetry collector. If the application developer chooses to export data without using the OpenTelemetry collector they MUST NOT do this without the end user's approval.

> **Note:** See the [application observability overview](../margo-overview/application-observability-overview.md) page for more information about application observablity.
>
> **Action:** Need to address in some form legacy applications that are not currently using open telemetry and don't want to migrate their application to use it.

