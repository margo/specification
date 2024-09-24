Observability involves the collection and analysis of information produced by a system to monitor its internal behavior.

Observability data is captured using the following signals:

- [Metrics](https://opentelemetry.io/docs/specs/otel/metrics/) - a numerical measurement in time used to observe change over a period of time or configured limits. For example, memory consumption, CPU Usage, available disk space.
- [Logs](https://opentelemetry.io/docs/specs/otel/logs/) - text outputs produced by a running system/application to provide information about what is happening. For example, outputs to capture security events such as failed login attempts, or unexpected conditions such as errors.  
- [Traces](https://opentelemetry.io/docs/specs/otel/trace/) - contextual data used to follow a request's entire path through a distributed system. For example, trace data can be used to identify bottlenecks, or failure points, within a distributed system.

Margo's application observability scope is limited to the following areas:

- The device's container platform
- The device's workload orchestration agent
- The compliant workloads deployed to the device.

The application observability data is intended to be used for purposes such as:

- Monitoring the container platform's health and current state. This includes aspects such as memory, CPU, and disk usage as well as cluster, node, pod, and container availability, run state, and configured resource limits. This enables end users to make decisions such as whether or not a device can support more applications, or has too many deployed.
- Monitoring the workload orchestration agent and containerized application's state to ensure it is running correctly, performing as expected and not consuming more resource than expected.
- To assist with debugging/diagnostics for applications encountering unexpected conditions impacting their ability to run as expected.

Margo's application observability is NOT intended to be used to monitor anything outside the device such as production processes, machinery, controllers, or sensors and should NOT be used for this purpose.

### Observability Framework

Application observability data is made available using [OpenTelemetry](https://opentelemetry.io/docs/). OpenTelemetry, a popular open source specification, defines a common way for observability data to be generated and consumed.

There are several reasons why OpenTelemetry was chosen:

- OpenTelemetry is based on a open source specification and not only an implementation
- OpenTelemetry is widely adopted
- OpenTelemetry has a large, and active, open source community
- OpenTelemetry provides [SDKs](https://opentelemetry.io/docs/languages/) for many popular languages if people wish to use them
- The OpenTelemetry community project has reusable components such as telemetry [receivers](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver) for Kubernetes, Docker and the host system making integration easier.
- OpenTelemetry is vendor agnostic.

See the following pages for information about application vendors [publishing observablity data](../app-interoperability/publishing-application-observability-data.md), devices [collection application observability data](../device-interoperability/collecting-application-observability-data.md), and workload orechestration solutions [consuming application observability data](../orchestration/workload/consuming-application-observability-data.md)

> **Decision Needed:** Need to determine which version(s) of the specification are supported