Usage
=====

**************
Pre-assessment
**************

The `pre-assessment assessment report <../../pre-assessment-report.md>`_ is to be completed using information provided
by the submitter. The assessor must also report on their experiences with verifying the submitted code for the
assessment, including the settings and parameters used.

*********************************
High-level performance assessment
*********************************

The high-level assessment covers the following 5 main rubrics:

1. Core
2. Intra-node
3. Inter-node
4. GPU
5. I/O

Details of how to conduct each performance measurement are given in
the `performance assessment guidebook <https://shareing-dri.github.io/performance-assessment/guidebook>`_. An
`example report <../../examples/stencil-example-report.md>`_ is also provided.

The ``high-level-plots.py`` script in the :ref:`assessmenttemplate` package can be used to
create the plots and metric required to fill out the `high-level assessment report <../../high-level-report.md>`_

.. _assessmenttemplate:

***********************************
The ``assessmenttemplate`` package
***********************************

The ``assessmenttemplate`` Python package and its few dependencies can be installed locally, or in a virtual
environment (recommended) optionally with `uv <https://docs.astral.sh/uv/pip/packages/#installing-a-package>`_, by running the command:

.. code-block:: bash

    pip install . # or uv pip install .

The package currently only contains modules to generate figures and metrics for that section of the high-level
assessment with the ``high-level-plots.py`` script :

.. code-block::

    usage: high-level-plots.py [-h] [--version] [-v] [-d] [--svg] [-i INPUT] [-o OUTPUT] [-s] [--show] {intranode,internode,summary} ...

    Tools to generate plots for the high-level assessment.

    positional arguments:
      {intranode,internode,gpu,summary}
                            Mode pertaining to the high-level rubric for which the plots are to be generated.

    options:
      -h, --help            show this help message and exit
      --version             Show program version number and exit.
      -v, --verbose         Print extra debug outputs.
      -d, --default         Output any requested outputs with unspecified file to their default file.
      --svg                 Output graph to default file will output SVG rather than PNG.
      -i, --input INPUT     Specify an optional input file containing the table for the metric.requested. Will use stdin if none specified.
      -o, --output OUTPUT   Specify an output file. This can only be used if exactly one output type is requested.
      -s, --stdout-graph    Output image data to stdout (useful for piping)
      --show                Show graph in window at runtime.

    Processes commandline arguments and the input table containing intranode/internode runtimes per core/thread/node counts, or high-level metrics per rubric. Input can be either a Markdown table or a CSV. Produces the relevant
    graph (line, point or spiderweb plot) and a Markdown formatted version of the input table with further processed data added (like parallel efficiency) if applicable. Unless an output flag is specified, a requested output will
    be echoed to the standard console output.

The script currently only offers two modes: :ref:`intranode-and-internode` and :ref:`summary`.
Further modules for the high-level, and scripts for the low-level assessment will be added in due course as the
methodology is developed. The "Core" and "I/O" rubrics do not require significant calculations to complete so no
associated scripts or modules will be created for them. As of 09-09-2026, the workflows and measurements required for
the GPU and internode metrics are still being established.

.. _intranode-and-internode:

===============================
``intranode`` and ``internode``
===============================
Intra-node and inter-node performance analysis figures are generated using the ``scaling`` module accessed with
``high-level-plots intranode`` and ``high-level-plots internode`` respectively. The usage information for the
``intranode`` mode is provided below and `internode`` uses the same arguments:

.. code-block::

    usage: high-level-plots.py intranode [-h] [-g [{cont,cat}]] [-m] [-c] [-a] [--graph-file GRAPH_FILE] [--markdown-file MARKDOWN_FILE] [--critical-points-file CRITICAL_POINTS_FILE]

    Generate a strong scaling efficiency graph and table from intra-node runtimes.

    options:
      -h, --help            show this help message and exit
      -g, --graph [{cont,cat}]
                            Generate graph; either a continuous line plot (cont; default) or a categorical point plot (cat).
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

    Unless an output flag is specified, a requested output will be echoed to the standard console output.

In the ``intranode`` mode, the script can take data input from the standard input, a unix pipe or a file. The
input is a table which can be in CSV or Markdown format. Suppose we have the following data saved as ``intranode_times.csv``:

.. code-block::
    
    Cores, Times
    1, 29.995
    2, 18.23
    4, 10.74
    8, 10.33
    16, 9.1307
    32, 8.5401
    64, 7.4589

where the first column is the core count and the second is the time in seconds. The graph can be checked
interactively by running:

.. code-block:: bash

    ./high-level-plots.py intranode --graph # or -g

and pasting the data when prompted. This will generate a plot in a separate window without saving it.
The default is a continuous line plot. For a categorical point plot use ``--graph cont``.

The script can also generate a Markdown table which can be copied to the report. To
generate it along with saving the graph to file, the following commands can be used:

.. code-block:: bash

    cat intranode_times.csv | ./high-level-plots.py -d intranode -mg --markdown-file=stdout
    # N.B. `-gm` will not work as the `m` will be interpreted as an input to `-g`

.. code-block:: md

    |   # Cores/threads |   Time (s) |   Parallel efficiency (%) |
    |------------------:|-----------:|--------------------------:|
    | 1                 | 29.995     | 1.000                     |
    | 2                 | 18.230     | 0.823                     |
    | 4                 | 10.740     | 0.698                     |
    | 8                 | 10.330     | 0.363                     |
    | 16                | 9.1307     | 0.205                     |
    | 32                | 8.5401     | 0.110                     |
    | 64                | 7.4589     | 0.063                     |

The script can also be provided a Markdown table in the above format as the input just like the CSV table. For
``intranode``, only the first two columns containing number of cores and execution time respectively will be read in.
For `internode`, the first column is expected to be the node count, and a third `"Relative problem size" <../../high-level-report.md#4-inter-node-assessment>`_
column is also expected.

By default (set with the ``--default`` or ``-d`` flag), the generated graph will be written to the ``images`` directory.

The ``scaling`` module contains three useful functions which could be used for other modules:

#. ``scaling_times_crit_80_60(times: list[tuple[int, float]]) -> tuple[float, float]`` - this calculates the 80%
   and 60% efficiency points and returns them as a tuple

#. ``scaling_times_to_graph(times: list[tuple[int, float]]) -> plt.Figure`` - self-explanatory, generates the graph

#. ``scaling_times_to_markdown(times: list[tuple[int, float]]) -> str`` - this renders the core counts and times as a
   three-column Markdown table with core count, time, and parallel efficiency

Each function is passed the times as a list of tuples of core count and time taken.

.. _gpu:

=======
``gpu``
=======

.. warning::
    The module can currently only be used for NVIDIA GPUs.

The ``gpu`` module contains functions that process the metrics generated
using the `Nsight Compute <https://developer.nvidia.com/nsight-compute>`_ profiling tool for NVIDIA GPUs for the GPU
assessment.

.. code-block::

    usage: high-level-plots.py gpu [-h]

    Compute the GPU score from the metrics collected from Nsight Compute for the SHAREing high-level performance assessment.

    options:
      -h, --help  show this help message and exit

The CSV generated from the tool (`as described here <../../high-level-report.md>`_) can be provided as input to the module as follows:

.. code-block:: bash

    cat ncu_metrics.csv | ./high-level-plots.py --output=stdout gpu

The module will then parse the input, filter for the `relevant metrics <../../high-level-report.md>`_, compute the total number of operations in the
profiled program, and produce a formatted Markdown table of the metrics:

.. code-block:: md
    
    | Metric                                              |   # operations |
    |:----------------------------------------------------|---------------:|
    | `sm__sass_thread_inst_executed_op_fp16_pred_on.sum` |      139462784 |
    | `sm__sass_thread_inst_executed_op_fp32_pred_on.sum` |      954130859 |
    | `sm__sass_thread_inst_executed_op_fp64_pred_on.sum` |    24513873492 |
    | Total                                               |    25607467135 |

The ``# operations`` value for the precision relevant for the assessed code is then used to compute the final GPU metric. 
The produced table, which can be printed to the terminal, written to the default file (``gpu_metrics.md``) with ``--default/-d`` 
or to one provided by the user via ``--output/-o``, can be copied to the high-level assessment report.


.. _summary:

===========
``summary``
===========

The ``summary`` module contains functions to generate the rubric summary graphics for the report:

.. code-block::

    usage: high-level-plots.py summary [-h] [-b]

    Generate a spiderweb diagram or bar graph for the SHAREing high-level performance assessment.

    options:
      -h, --help  show this help message and exit
      -b, --bar   Output a bar chart instead of a spiderweb.

When called with the ``summary`` mode, the ``high-level-plots.py`` script takes data input from the standard input, UNIX
pipe or input file, as either a CSV or Markdown table. It accepts an arbitrary
number of rows of "metric, score".
