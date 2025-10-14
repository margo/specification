# Personas

Throughout this documentation, the following personas are used to represent interaction with the standard and/or with entities defined by the standard.

## Persona Relationships
![Persona Relationships](../figures/persona-relationship.drawio.svg)

## Categories

These categories group common personas together under a shared goal or role. These categories will be used in other documentation to provide grouping and clarity where appropriate.

### End Users
- Evaluates the best-in-class products offered by the suppliers
- Consumes products provided by the suppliers
- Assembles multiple vendor's products into a productive automation system

### Suppliers
- Contribute knowledge and expertise to the specification sections relevant to their business.
- Builds products compliant with the Margo specification.
- Markets and sells their products to end users

## Persona Definitions

These persona definitions represent individual entities with specified use cases and requirements, aligned with the other personas in their category.

### End Users

End users consume products and technologies that adopt the specification to deliver desired business outcomes. 

#### OT User

Consumer of functionality provided by the application vendors to run critical and non-critical business functions, or to improve business efficiency

#### OT Architect

Creates and enforces standards across OT deployment locations or sites for greater supportability and consistency

#### Integrator

Optional persona, external to the organization of the other end user personas, but tasked with assembling and installing hardware and software provided by the suppliers

#### IT Service Provider

Provides "IT-like" services, such as connectivity, backup and restore, automation, security and auditing, within the End User's OT environment. 

### Suppliers

Suppliers provides hardware or software that's evaluated and deployed by the end users

#### Workload Supplier

Provides an application that performs some desired function, such as computer vision, software-defined control, etc, which is deployed to device via a Workload Fleet Manager

#### Fleet Management Supplier

Provides a software package that enables End Users to manage their workloads and/or devices the workloads run on via Fleet management patterns.

#### Device Supplier

Provides hardware resources, such as CPU and memory, along with lifecycle support, such as firmware and BIOS updates

#### Platform Supplier

Provides operating system level software to abstract hardware resources, and optionally, container orchestration software on top of the the operating system layer