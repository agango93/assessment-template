# Durham hardware systems information

The following are hardware tables for systems based at Durham which are frequently used for the assessments.

## Hamilton

The hardware details for Hamilton are [available here](https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-su/computer/systems/). This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session:

| Specification | Details |
| -------------- | ------------------------------------------------ |
| Number of compute nodes | Standard: 120; High-memory: 2 |
| Processors / node | 2 $\times$ [AMD EPYC 7702 64-Core Processors](https://www.amd.com/en/support/downloads/drivers.html/processors/epyc/epyc-7002-series/amd-epyc-7702.html) |
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

## Bede

The hardware details for Bede are [available here](https://bede-documentation.readthedocs.io/en/latest/hardware/index.html). This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session:

| Specification               | Details                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Processors / node           | 2 $\times$ [POWER9 CPU](https://www.redbooks.ibm.com/redbooks.nsf/pages/power9?Open) |
| Clock speed / CPU           | Base: 2700 MHz; Boost: 3800 MHz                                                      |
| Sockets / node              | 2                                                                                    |
| Cores / socket              | 40                                                                                   |
| NUMA domains / socket       | 1                                                                                    |
| Cache                       | 32KB L1i/32KB L1d / core, 512KB L2 / core and 10MB L3 Cache size / 4-core chiplet    |
| Simultaneous Multithreading | 4 threads / core                                                                     |
| RAM / node                  | 512GB DDR4                                                                           |
| GPUs / node                 | 4 $\times$ [Nvidia Tesla V100 32GB](https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf) |
| GPU interconnect            | [NVLink](https://www.nvidia.com/en-gb/data-center/nvlink/) 2.0                       |
| Interconnect                | 2 $\times$ Mellanox EDR (100Gbit/s) InfiniBand ports, organised in a 2:1 block fat tree topology |

Additionally, there is the `infer` partition with Tesla T4 GPUs and 7 Grace Hopper nodes in a separate partition.
