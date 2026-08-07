# Custom Runtimes and Deployments

Application suppliers may require a way to package and deploy applications using a deployment type or runtime that goes beyond what is defined in the Margo specification.

The functionality is supported via custom runtime and deployment types and may be used for collaboration between application and device suppliers to deploy non-Margo standarized workloads.

While custom runtime and deployment types are not interoperable by nature, a standardized mechanism ensures that such extensibility concerns do not break interoperability or conformance for other suppliers, that unknown runtime and deployment types are safely ignored, and that the Margo specification can evolve without breaking supplier-specific use cases.

The use of custom runtimes and deployment types adds functionality that is not part of the Margo specification. It is expected suppliers collaborate with each other in order to know what is available. Margo does not maintain a listing of these custom runtime or deployment type labels.

For specifics, see the specification extension documentation for each of the following documents:

- [Application Description](../applications/application-description.md#specification-extensions)
- [Application Deployment](./desired-state#specification-extensions)
- [Device Capabilities](./device-capabilities.md#specification-extensions)


