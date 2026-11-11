# Durham hardware systems information

The following are hardware tables for systems based at Durham which are frequently used for the assessments.

## Hamilton

The hardware details for Hamilton are [available here](https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-su/computer/systems/). This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session. There are 120 standard compute nodes on the system:

| Specification | Details |
| -------------- | ------------------------------------------------ |
| Number of compute nodes | Standard: 120; High-memory: 2 |
| Processors | 2 $\times$ [AMD EPYC 7702 64-Core Processors](https://www.amd.com/en/support/downloads/drivers.html/processors/epyc/epyc-7002-series/amd-epyc-7702.html) |
| Clock speed / CPU | Base: 2000 MHz; Boost: 3350 MHz |
| Sockets / node | 2 |
| Cores / node | 64 |
| NUMA domains | 8 / node (4 / socket), each with a dedicated memory channel and further split into 4 groups containing 4 cores each |
| Cache | 16 MB L3 cache / 4-core chiplet, 512 KB of L2 cache / core and 32 KB of L1 cache / core |
| Chiplets / NUMA domain | 4 |
| Simultaneous Multithreading | Disabled
| RAM / node | Standard: 256 GB DDR4 (246 GB available to users); High-memory: 2 TB DDR4 |
| Local storage | 400GB SSD |
| Interconnect | Infiniband HDR 200GB/s high /formance interconnect, with a 2.6:1 fat tree topology formed of non-blocking islands of up to 26 nodes |

Hamilton also has one GPU node with the following configuration verified with `cat /proc/cpuinfo` and `nvidia-smi`:

| Specification | Details |
| ------------- | ------- |
| Processors | [2 AMD EPYC 9555 64-Core Processors](https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9555.html) |
| GPUs | 8 NVIDIA H200 NVL |
| RAM | 2.2 TB |
| Local storage | 3 TB NVMe |
