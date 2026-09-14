---
License: Copyright © 2026 Durham University, SHAREing Project, MIT Licensed
Creator: Thomas Flynn
Contributors: Thomas Flynn, Emily Wilkinson, Ananya Gangopadhyay
Summary: README file for the SHAREing assessment templates repository
---

# <img src='./images/logo.svg' width=90 style="vertical-align:middle" /> SHAREing: Performance Assessment Templates

> [!WARNING]
> This repository is currently under development.

This repository contains Markdown templates to write reports for [SHAREing](https://shareing-dri.github.io/)'s
Performance Assessment service.

It also includes and a Python package to generate graphics and metrics required to fill the report. Currently, it can
only be used for some of the rubrics in the high-level assessment.

## Pre-assessment

The [pre-assessment assessment report](reports/pre-assessment-report.md) is to be completed using information provided
by the submitter. The assessor must also report on their experiences with verifying the submitted code for the
assessment, including the settings and parameters used.

## High-level performance assessment

The high-level assessment covers the following 5 main rubrics:

1. Core
2. Intra-node
3. Inter-node
4. GPU
5. I/O

Details of how to conduct each performance measurement are given in
the [performance assessment guidebook](https://shareing-dri.github.io/performance-assessment/guidebook). An [
`example report`](examples/stencil-example-report.md) is also provided.

## The `assessmenttemplates` package

The `assessmenttemplates` Python package and its few dependencies can be installed locally, or in a virtual environment,
by running the command:

```shell
pip install .
```

The package currently only contains modules to generate figures and metrics for that section of the high-level
assessment with the `high-level-plots.py` script :

```txt
usage: high-level-plots.py [-h] [--version] [-v] [-d] [--svg] [-i INPUT] [-o OUTPUT] [-s] [--show] {intranode,summary} ...

Tools to generate plots for the high-level assessment.

positional arguments:
  {intranode,summary}  Mode pertaining to the high-level rubric for which the plots are to be generated.

options:
  -h, --help           show this help message and exit
  --version            Show program version number and exit.
  -v, --verbose        Print extra debug outputs.
  -d, --default        Output any requested outputs with unspecified file to their default file.
  --svg                Output graph to default file will output SVG rather than PNG.
  -i, --input INPUT    Specify an optional input file containing the table for the metric.requested. Will use stdin if none specified.
  -o, --output OUTPUT  Specify an output file. This can only be used if exactly one output type is requested.
  -s, --stdout-graph   Output image data to stdout (useful for piping)
  --show               Show graph in window at runtime.

Unless an output flag is specified, a requested output will be echoed to the standard console output.
```

The script currently only offers two modes: [`intranode`](#intranode) and [`summary`](#summary). Further modules for the
high-level, and scripts for the low-level assessment will be added in due course as the methodology is developed. The
"Core" and "I/O" rubrics do not require significant calculations to complete so no associated scripts or modules will be
created for them. As of 09-09-2026, the workflows and measurements required for the GPU and internode metrics are still
being established.

### `intranode`

Intra-node performance analysis figures are generated using the `intranode` module, accessed with
`high_level_assessment.py intranode`:

```txt
usage: high-level-plots.py intranode [-h] [-g] [-m] [-c] [-a] [--graph-file GRAPH_FILE] [--markdown-file MARKDOWN_FILE] [--critical-points-file CRITICAL_POINTS_FILE]

Generate a strong scaling efficiency graph and table from intra-node runtimes.

options:
  -h, --help            show this help message and exit
  -g, --graph           Generate graph.
  -m, --markdown        Generate markdown table.
  -c, --critical-points
                        Calculate 80 and 60 percent critical values.
  -a, --output-all      Output all output types.
  --graph-file GRAPH_FILE
                        Specify an output file for the graph.
  --markdown-file MARKDOWN_FILE
                        Specify an output file for the markdown table.
  --critical-points-file CRITICAL_POINTS_FILE
                        Specify an output file for the calculated critical values.

Unless an output flag is specified, a requested output will be echoed to the standard console output. This script may be passed either a Markdown table containing thread count, time, and (optional) parallel efficiency, or by
passing CSV thread count, time. It can output a matplotlib graph and a Markdown formatted table with all three columns filled in.
```

In the `intranode` mode, the script can take data input from the standard input, a unix pipe or a file. The input is a
table which can be in CSV or Markdown format. Suppose we have the following data saved as `times.csv`:

```csv
1, 29.995
2, 18.23
4, 10.74
8, 10.33
16, 9.1307
32, 8.5401
64, 7.4589
```

where the first column is the core count and the second is the time in seconds. The graph can be generated interactively
by running:

```shell
$ ./high-level-plots.py intranode --graph
```

and pasting the data when prompted. The script can also generate a Markdown table which can be copied to the report:

```shell
$ cat times.csv | ./high-level-plots.py intranode -gmd --markdown-file=stdout
```

```md
| Thread count | Time (s) | Parallel Efficiency |
|--------------|----------|---------------------|
| 1            | 29.995   | 1.000               |
| 2            | 18.230   | 0.823               |
| 4            | 10.740   | 0.698               |
| 8            | 10.330   | 0.363               |
| 16           | 9.1307   | 0.205               |
| 32           | 8.5401   | 0.110               |
| 64           | 7.4589   | 0.063               |
```

The script can also be provided a Markdown table in the above format as the input just like the CSV table.

By default (set with the `--default` or `-d` flag), the generated graph will be written to the [`images`](images)
directory.

The `intranode` module contains three useful functions which could be used for other modules:

1. `intranode_times_crit_80_60(times: list[tuple[int, float]]) -> tuple[float, float]` - this calculates the 80% and 60%
   efficiency points and returns them as a tuple
2. `intranode_times_to_graph(times: list[tuple[int, float]]) -> plt.Figure` - self-explanatory, generates the graph
3. `intranode_times_to_markdown(times: list[tuple[int, float]]) -> str` - this renders the core counts and times as a
   three-column Markdown table with core count, time, and parallel efficiency

Each function is passed the times as a list of tuples of core count and time taken.

### `summary`

The `summary` module contains functions to generate the rubric summary graphics for the report:

```txt
usage: high-level-plots.py summary [-h] [-b]

Generate a spiderweb diagram or bar graph for the SHAREing high-level performance assessment. This script may be passed either a Markdown table containing thread count, time, and (optional) parallel efficiency, or by passing
CSV thread count, time. It can output a matplotlib graph and a Markdown formatted table with all three columns filled in.

options:
  -h, --help  show this help message and exit
  -b, --bar   Output a bar chart instead of a spiderweb.
```

When called with the `summary` mode, the `high-level-plots.py` script takes data input from the standard input, unix
pipe or input file the same way as the `intranode` mode, as either a CSV or Markdown table. It accepts an arbitrary
number of rows of "metric, score".

## Contributions

This performance assessment is intentionally limited as we want to simply capture the performance of software at a *high
level*. However, if you have ideas of performance metrics which are necessary but missing, or if you find any faults
with the scripts or template, please raise an issue.

## Acknowledgements

The initial development of the notebook was implemented by Ben Clark. Further work on the notebook was undertaken by
Thomas Flynn, before it was rewritten as scripts. This project has received funding through the UKRI Digital Research
Infrastructure Programme under grant UKRI1801 (SHAREing).

<img src='./images/ukri.png' width=200 style="vertical-align:middle" alt="UKRI logo"/> 

All files in this repository are released under the [MIT License](./LICENSE).
