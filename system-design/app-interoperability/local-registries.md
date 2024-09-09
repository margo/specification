# Local Registries

This section investigates options for configuring the usage of local Docker (or Helm Chart) registries. The goal of configuring such local registries is to avoid the reliance on public, Internet-accessible registries. The reasons for not using such public registries are mainly twofold: (1) publicly hosted Docker images or Helm charts could become unavailable at some point, as the owner decides to take the Docker images or Helm charts off the public registry, (2) Internet connectivity may not be available to the device and hence public registries are not reachable, or (3) end-users want to host their own registries so they can do security scans and validate the packages.

In terms of connectivity, we can thereby distinguish mainly between the following device categories:

1.	**Fully connected device**, which means a device is deployed in the field (e.g., a factory shop floor) and has access to the Internet.
2.	**Locally connected device**, i.e., the device has connectivity to a local network (e.g., factory- or enterprise-wide) and a local repository can be made reachable.
3.	**Air-gapped device**, i.e., the device generally is not connected and must be configured by accessing it directly (via USB, Bluetooth, or a direct network link, e.g., via Ethernet cable, or similar) for example via a technician’s laptop.

Local registries for Docker images and Helm Charts can be used for all 3 categories of devices. In case of **fully connected devices**, although the device could reach the Internet, a local registry can still be useful, e.g., as a cache for remote registries to save on bandwidth or to have Docker images and Helm Carts reliably available. In case of **locally connected devices**, a local registry is required to enable the WOA to install margo applications on the device, as the device/WOA does not have Internet access. Thereby, the local registry can be setup as a _pull-through cache_ where data (e.g., Docker images) are cached locally when they are first retrieved from a remote source and subsequent requests for the same data are served from the local cache rather than fetching it again from the remote source. In case of **air-gapped devices**, a local registry has to be accessible on the technician's laptop (or other directly connected device), which performs the application installation process.

To setup local registries, different configuration options exist:

## Option - Docker Registry Mirror on Kubernetes Level

Kubernetes supports the configuration of registry mirrors. How this is configured depends on the distribution and the underlying container runtime. Distributions that utilize **containerd** as runtime (e.g., k3s or microk8s) allow the definition of mirrors in a configuration file. For example, in k3s the file `/etc/rancher/k3s/registries.yaml` can be used to set up a mirror for each device's Kubernetes environment:

```
mirrors:
  "docker.io":
    endpoint:
      - "http://<local-registry-ip>:5000"
configs:
  "docker.io":
    auth:
      username: "<username>"
      password: "<password>"
```

## Option - Docker Registry as Pull-through Cache on Docker Level

To configure a pull-through cache in Docker for the container registry, a Docker Registry can be setup that acts as caching proxy for a remote Docker registry. Such a Docker Registry container can be defined using the following `config.yml`:

```
version: 0.1
log:
  fields:
    service: registry
storage:
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
proxy:
  remoteurl: https://registry-1.docker.io
```

This registry can be started uing the following command:
`docker run -d -p 5000:5000 --restart unless-stopped --name registry -v $(pwd)/config.yml:/etc/docker/registry/config.yml registry:2`

Then, the Docker daemon needs to be configured to use the private registry as a mirror in the `/etc/docker/daemon.json` file:
```
{
  "registry-mirrors": ["http://10.100.2.102:5000"],
  "insecure-registries": ["10.100.2.102:5000"]
}
```

## Option - Helm Chart Registry as Pull-through Cache

Setting up a pull-through cache for Helm charts in combination with Kubernetes involves configuring a local Helm chart repository, e.g., ChartMuseum that can be installed with the `PROXY_CACHE` variable set to `true`:

```
helm repo add chartmuseum https://chartmuseum.github.io/charts
helm repo update
helm install my-chartmuseum chartmuseum/chartmuseum --set env.open.DISABLE_API=false --set env.open.PROXY_CACHE=true
```

Then, this Helm Chart repository can be added to Helm and chart releases can be installed there:

```
helm repo add my-cached-repo http://<chartmuseum-ip>:8080
helm repo update
helm install my-release my-cached-repo/<chart-name>

```
Now, when deploying applications in Kubernetes using Helm, the cached repository is used to serve charts rather than the remote repository.
