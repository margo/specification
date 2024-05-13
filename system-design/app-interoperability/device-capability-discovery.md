# Margo Device Capability Discovery 

The Workload Orchestration Software is informed of the Device Capabilities. This information is provided to the Workload Orchestration Software by the Workload Orchestration Agent interface. 

## Device Capability Required Information
The Device Owner shall provide a file that describes the capabilities and characteristics of their Device. The purpose of the capability file is to ensure the WOS has the information needed to pair Workloads with the appropriate Edge Device. The capabilities file is provided by the Workload Orchestration Agent to the WOS during the enrollment process.  

The following information is required to be present:

- Device Vendor
- Model Number
- Serial Number
- Margo Device Role Designation(Cluster Leader/Worker / Standalone Device)
- CPU Architecture(ARM/Intel)
- Number of vCPUs
- Memory Capacity
- Storage Capacity
- Device interfaces or peripherals(i.e. Graphics card V. X.X.X)
- Network interfaces(wifi/eth/cellular)
- Container Runtime(Kubernetes / Docker compose)


## Device Capabilitiy File format
The Margo Device Capability file shall be formatted as a XXX File.

> **Investigation Needed:** Further Investigation needed on this strategy. 

## Device Capability Storage Standards
It is important to ensure the Workload Orchestration Agent has access to the capabilities folder. 
Folder shall be structured as such. 


![Device Capability Discovery (svg)](../figures/Workload-orchestration-node-capability-discovery.drawio.svg)




