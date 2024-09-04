#Local Registries

This section investigates options for configuring the usage of local Docker (or Helm Chart) registries. The goal of configuring such local registries is to avoid the reliance on public, Internet-accessible registries. The reasons for not using such public registries are mainly twofold: (1) publicly hosted Docker images or Helm charts could become unavailable at some point, as the owner decides to take the Docker images or Helm charts off the public registry, or (2) Internet connectivity may not be available to the device and hence public registries are not reachable.

In terms of connectivity, we can thereby distinguish mainly between the following device categories:

1.	Fully connected device, which means a device is deployed in the field (e.g., a factory shop floor) and has access to the Internet.
2.	Locally connected device, i.e., the device has connectivity to a local network (e.g., factory- or enterprise-wide) and a local repository can be made reachable.
3.	Air-gapped device, i.e., the device generally is not connected and must be configured by accessing it directly (via USB, Bluetooth, or a direct network link, e.g., via Ethernet cable, or similar) for example via a technician’s laptop.
