# Specification Extensions

Workload fleet manager and device suppliers may desire a way to add custom metadata, configuration, or functionality to certain Margo documents that goes beyond what is defined in the Margo specification. 

The functionality is supported via specification extensions and may be used for:

- Collaboration between application and workload fleet manager suppliers
- Collaboration between application and device suppliers
- Collaboration between workload fleet manager and device suppliers

While specification extensions are not interoperable by nature, a standardized extension mechanism ensures that such customizations do not break interoperability or conformance for other suppliers, that unknown extensions are safely ignored, and that the Margo specification can evolve without breaking supplier-specific customizations.

Specification extensions add functionality that is not part of the Margo specification. It is expected suppliers collaborate with each other in order to know what is available. Margo does not maintain a listing of these specification extensions.

Workload fleet management server and client implementations MUST NOT fail when encountering unknown specification extensions in the Application Description, Application Deployment or Device Capabilities documents. Unknown specification extension properties targeting a workload fleet manager or device supplier MUST be ignored.

For specifics, see the specification extension documentation for each of the following documents:

- [Application Description](../applications/application-description.md#specification-extensions)
- [Application Deployment](./desired-state#specification-extensions)
- [Device Capabilities](./device-capabilities.md#specification-extensions)

The property naming conventions for adding specification extension is `x-<unique name>-extensions`. 

The `<unique-name>` MUST match the `[a-z][a-z0-9-]*` regular expression and conform with the following rules:

- MUST start with a lowercase letter
- MUST have no spaces or special characters 
- MAY contain lowercase letters, digits, and dashes

It is recommended to use identifying information as the unique name such as a company name, organization name, a combination of company name and department, etc. to reduce chances of naming conflicts.

For example:

- x-acme-extensions
- x-edgecircuitsystems-extensions
- x-northstar-industries-extensions
- x-northforgesystems-processautomation-extensions

The value of an extension property MUST be an object (a YAML/JSON mapping). Its child properties may be any simple or complex structure, as long as it is valid YAML or JSON applicable to the document type the specification extension property is added to.

> **Note:** The supplier implementing the specification extension defines the specification extension property name and supported child properties. A supplier wishing to make use of the specification extension uses the specification extension property name and child properties the implementor has defined.
