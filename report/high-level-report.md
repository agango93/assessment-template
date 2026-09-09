---
License: Copyright © 2026 Durham University, SHAREing Project, MIT Licensed
Creator: Emily Wilkinson
Contributors: Emily Wilkinson
Summary: High-level assessment report template
---

# <img src='./images/logo.svg' width=90 style="vertical-align:middle" /> SHAREing: High-level performance assessment report

## Setup Details

* Program:
* Parallel model:
* Dependencies:
* Compiler:
* Compiler flags:
* Problem spec:

## CPU Analysis

For a basic high-level analysis of CPU performance, we look for the floating-point operation rate compared to the
theoretical rate for the CPU.

The hardware capabilities were determined with

```bash
$ 
```

The software CPU compute rate was determined with

```bash
$ 
```

|          | MFLOP/s | 
|----------|---------|
| CPU      |         |
| Measured |         |

We determine this software to have a CPU score of `X`.

## GPU Analysis

For a basic high-level analysis of GPU performance, we look for the average occupancy of the GPU floating-point modules.

The theoretical GPU compute rate is `X MFLOPS/s`.

The software GPU compute rate was determined with

```shell
$ 
```

|          | MFLOP/s |
|----------|---------|
| GPU      |         |
| Measured |         |

We determine this software to have a GPU score of `X`.

## IO Analysis

For a basic high-level analysis of IO performance, we look for the proportion of the runtime spent processing IO
requests.

The IO time was determined with

```shell
$ 
```

The IO utilisation ratio is `X`, and the IO score is `1-X`.

## Intra-node Analysis

For a basic high-level analysis of intra-node performance, we perform a strong scaling by fixing the problem size and
increasing core allocation.

For this code, we tested with core counts in powers of 2 from 1 to 64.

| Thread count | Time (s) | Parallel Efficiency |
|--------------|----------|---------------------|
| 1            |          |                     |
| 2            |          |                     |
| 4            |          |                     |
| 8            |          |                     |
| 16           |          |                     |
| 32           |          |                     |
| 64           |          |                     |

Hence, our 80% threshold is at `X` cores and our 60% threshold is at `Y` cores. As a proportion of the number of cores
available, which is `Z` on the node this was run on, this gives a score of `X/Z` and `Y/Z`.

<img src='../images/intranode.png' width=500 />

## Inter-node Analysis

For a basic high-level analysis of inter-node performance, we perform a weak scaling by increasing problem size linearly
with node allocation.

## Summary

The following table collates the results of all above sections. These scores are indicative only, and cannot truly be
compared to one another meaningfully without taking into account domain knowledge and methodological differences between
them.

| Result           | Score | Metric result |
|------------------|-------|---------------|
| CPU              |       |               |
| GPU              |       |               |
| IO               |       |               |
| Intra-node (80%) |       |               |
| Inter-node (80%) |       |               |

<img src='../images/summary.png' width=500 />