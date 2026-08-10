# Custom Runtimes and Deployments

Application suppliers may require a way to package and deploy applications using a deployment type or runtime that goes beyond what is defined in the Margo specification.

The functionality is supported via custom runtime and deployment types and may be used for collaboration between application and device suppliers to deploy non-Margo standardized workloads.

While custom runtime and deployment types are not interoperable by nature, a standardized mechanism ensures that such extensibility concerns do not break interoperability or conformance for other suppliers, that unknown runtime and deployment types are safely ignored, and that the Margo specification can evolve without breaking supplier-specific use cases.

The use of custom runtimes and deployment types adds functionality that is not part of the Margo specification. It is expected suppliers collaborate with each other in order to know what is available. Margo does not maintain a listing of these custom runtime or deployment type labels.

For specifics, see the documentation for each of the following documents:

- [Application Description](../applications/application-description.md#custom-runtimes-and-deployments)
- [Device Capabilities](../margo-management-interface/device-capabilities.md#custom-runtimes-and-deployments)
- [Application Deployment](../margo-management-interface/desired-state#deviceconstraints-attributes)

Application suppliers MUST follow the same pattern established for officially support deployment types and use an OCI blob to package their application artifacts and use the existing Application Description [component properties](../applications/application-description#componentproperties-attributes) to describe its location. The specific details for how this OCI blob is created (e.g, metadata, layers, contents) are the responsibility of the suppliers to agree upon and are outside the scope of Margo's specification.

Device suppliers supporting a custom runtime or deployment type MUST follow the [Device Capabilities](../margo-management-interface/device-capabilities.md#custom-runtimes-and-deployments) guidelines to report these capabilities.