# Local Registries

This section investigates options for configuring the usage of local Docker (or Helm Chart) registries. The goal of configuring such local registries is to avoid the reliance on public, Internet-accessible registries. The reasons for not using such public registries are mainly twofold: (1) publicly hosted Docker images or Helm charts could become unavailable at some point, as the owner decides to take the Docker images or Helm charts off the public registry, or (2) Internet connectivity may not be available to the device and hence public registries are not reachable.

In terms of connectivity, we can thereby distinguish mainly between the following device categories:

1.	**Fully connected device**, which means a device is deployed in the field (e.g., a factory shop floor) and has access to the Internet.
2.	**Locally connected device**, i.e., the device has connectivity to a local network (e.g., factory- or enterprise-wide) and a local repository can be made reachable.
3.	**Air-gapped device**, i.e., the device generally is not connected and must be configured by accessing it directly (via USB, Bluetooth, or a direct network link, e.g., via Ethernet cable, or similar) for example via a technician’s laptop.

Local registries for Docker images and Helm Charts can be used for all 3 categories of devices. In case of fully connected devices, although the device could reach the Internet, a local registry can still be useful, e.g., as a cache for remote registries to save on bandwidth or to have Docker images and Helm Carts reliably available. In case of locally connected devices, a local registry is required to enable the WOA to install margo applications on the device, as the device/WOA does not have Internet access. Thereby, the local registry can be setup as a ''pull-through cache'' where data (e.g., Docker images) are cached locally when they are first retrieved from a remote source and subsequent requests for the same data are served from the local cache rather than fetching it again from the remote source. In case of air-gapped devices, a local registry has to be accessible on the technician's laptop (or other directly connected device), which performs the application installation process.

To setup local registries, different configuration options exist. 

## 