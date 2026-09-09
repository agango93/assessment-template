#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def intranode_times_crit_80_60(times: list[tuple[int, float]]) -> tuple[float, float]:
    """ 
    Calculate the 80% and 60% critical proportions

    :param times: list of (core count, time taken in seconds)
    :return: 80% proportion, 60% proportion
    """
    # Extract core count and times from the list as separate arrays
    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0] * core_counts[0]

    # Calculate efficiency and 80%/60% critical core points
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts

    p_crit_80 = float(max(core_counts[efficiency >= 0.8]))
    p_crit_60 = float(max(core_counts[efficiency >= 0.6]))

    intra_node_prop_80 = p_crit_80 / float(max(core_counts))
    intra_node_prop_60 = p_crit_60 / float(max(core_counts))

    return intra_node_prop_80, intra_node_prop_60


def intranode_times_to_graph(times: list[tuple[int, float]], args=None) -> plt.Figure:
    """ 
    Create matplotlib graph

    :param times: list of (core count, time taken in seconds)
    :param args: arguments from arg parser
    :return: matplotlib figure

    """

    # Extract core count and times from the list as separate arrays
    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0] * core_counts[0]

    # Calculate efficiency and 80%/60% critical core counts
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts
    if args and args.verbose:
        print(f"Calculated efficiencies: {efficiency}")

    p_crit_80 = float(max(core_counts[efficiency >= 0.8]))
    p_crit_60 = float(max(core_counts[efficiency >= 0.6]))

    fig, ax = plt.subplots()
    ax.set_xlabel(r'$p$')
    ax.set_ylabel(r'$E(p)$')

    ax.axvline(x=p_crit_80, color="#ffc844", linestyle="--")
    ax.text(p_crit_80, 0.05, "80%", rotation=90)
    ax.axvline(x=p_crit_60, color="#e35555", linestyle="--")
    ax.text(p_crit_60, 0.05, "60%", rotation=90)
    ax.plot(core_counts, efficiency, '.-', color="black", linewidth=2)

    ax.set_title("Intra-node strong scaling efficiency", fontsize=14)

    return fig


def intranode_times_to_markdown(times: list[tuple[int, float]]) -> str:
    """
    Generate Markdown table with
    """

    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0] * core_counts[0]

    # Calculate efficiency and 80%/60% critical core counts
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts

    header = "| Thread count | Time (s) | Parallel efficiency |\n| --- | ------- | ----- |"
    lines = [header]

    # If we assert that these are equal, we can use one length in the for loop.
    assert (len(core_counts) == len(parallel_times))
    for i in range(len(core_counts)):
        line = f"| {int(core_counts[i]):3d} | {parallel_times[i]:7.03f} | {efficiency[i]:5.03f} |"
        lines.append(line)

    return "\n".join(lines)


def intranode_add_args(main_parser):
    parser = main_parser.add_parser("intranode",
                                    description="Generate a strong scaling efficiency graph and table from intra-node "
                                                "runtimes.",
                                    epilog="Unless an output flag is specified, a requested output will be echoed to "
                                           "the standard console output." + intranode_main.__doc__
                                    )

    parser.add_argument("-g", "--graph", action="store_true", help="Generate graph.")
    parser.add_argument("-m", "--markdown", action="store_true", help="Generate markdown table.")
    parser.add_argument("-c", "--critical-points", action="store_true",
                        help="Calculate 80 and 60 percent critical values.")
    parser.add_argument("-a", "--output-all", action="store_true", help="Output all output types.")
    parser.add_argument("--graph-file", help="Specify an output file for the graph.",
                        default='images/intranode.png')
    parser.add_argument("--markdown-file",
                        help="Specify an output file for the markdown table.",
                        default='intranode_table.md')
    parser.add_argument("--critical-points-file",
                        help="Specify an output file for the calculated critical values.",
                        default='intranode_critical_proportions.txt')


def intranode_parse_args(unparsed_args):
    args = unparsed_args
    if args.verbose:
        print(f"args: {args}")

    if args.output_all:
        args.graph = True
        args.markdown = True
        args.critical_points = True

    if args.default:
        if args.verbose:
            print(f"Using default files.")
        args.graph_file = 'images/intranode.svg' if args.svg else 'images/intranode.png'

    if args.svg and (args.default or args.graph_file or (args.graph and args.output)):
        print(
            "WARNING: svg flag only has an effect when outputting to the default file. "
            "Matplotlib will output to svg if you specify a filename with file ending '.svg'")

    if args.graph + args.markdown + args.critical_points >= 2 and args.output:
        print("ERROR: Single specified output file is not valid when multiple outputs are requested at once.")
        exit()

    if args.output and args.output != "stdout":
        # Only one of the following is possible
        if args.graph:
            args.graph_file = args.output
        elif args.markdown:
            args.markdown_file = args.output
        elif args.critical_points:
            args.critical_points_file = args.output

    # "stdout" acts as an undocumented magic file to redirect an output to stdout if the default flag is set.
    # This makes it easier to send one output to default and one to stdout without having to know what the default
    # file is.
    if args.stdout_graph and args.graph_file:
        if args.graph_file == "stdout":
            print("WARNING: Graph file does not need to be specified as 'stdout' if '-s' flag specified.")
        else:
            print("WARNING: Requested to output graph to both stdout and a file. Limiting to only requested file.")
            args.stdout_graph = None
    if args.graph_file == "stdout":
        args.graph_file = None
        args.stdout_graph = True
    if args.markdown_file == "stdout":
        args.markdown_file = None
    if args.critical_points_file == "stdout":
        args.critical_points_file = None

    if not args.graph and not args.markdown and not args.critical_points:
        print("WARNING: No output specified, defaulting to graph only.")
        args.graph = True

    return args


def intranode_main(unparsed_args):
    """
    This script may be passed either a Markdown table containing thread count, time, and (optional) parallel efficiency,
    or by passing CSV thread count, time.

    It can output a matplotlib graph and a Markdown formatted table with all three columns filled in.
    """

    args = intranode_parse_args(unparsed_args)

    is_pipe = False

    lines = []

    if args.input:
        with open(args.input, 'r') as input_table:
            lines = input_table.readlines()
    else:
        is_pipe = not os.isatty(sys.stdin.fileno())

        if not is_pipe:
            print(f"Please paste the data below, ending with an empty line:")

        for line in sys.stdin:
            if line.strip() == '':
                break
            lines.append(line)

    ####################
    # INPUT PROCESSING #
    ####################

    if args.verbose:
        print("STATUS: processing input")

    if (args.input or is_pipe) and args.verbose:
        print("Inputted table:")
        print("".join(lines))

    if lines[0][0] == '|':
        lines = lines[2:]
        lines = map(lambda l: list(map(lambda s: s.strip(), l.split('|')))[1:-2], lines)
    else:
        split_commas = lambda l: l.split(',')
        lines = map(split_commas, lines)

    lines = list(lines)
    if args.verbose:
        print(f"lines: {lines}")

    strings_to_numbers = lambda l: (int(l[0]), float(l[1]))
    times = list(map(strings_to_numbers, lines))
    if args.verbose:
        print(f"times: {times}")

    #####################
    # OUTPUT GENERATION #
    #####################

    if args.graph:
        if args.verbose:
            print("STATUS: generating graph")
        fig = intranode_times_to_graph(times, args)
        if args.graph_file:
            # Ensure output directory exists
            if '/' in args.graph_file:
                os.makedirs(os.path.dirname(args.graph_file), exist_ok=True)
            # Save figure to file
            fig.savefig(args.graph_file)
        if args.show:
            plt.show()
        if args.stdout_graph:
            fig.savefig(sys.stdout)

    if args.markdown:
        if args.verbose:
            print("STATUS: generating markdown")
        table = intranode_times_to_markdown(times)
        if args.markdown_file:
            # Ensure output directory exists
            if '/' in args.markdown_file:
                os.makedirs(os.path.dirname(args.markdown_file), exist_ok=True)
            # Write to file
            with open(args.markdown_file, "w") as file:
                file.write(f"{table}")
        else:
            print(f"{table}\0")

    if args.critical_points:
        if args.verbose:
            print("STATUS: calculating critical points")
        points = intranode_times_crit_80_60(times)
        if args.critical_points_file:
            # Ensure output directory exists
            if '/' in args.critical_points_file:
                os.makedirs(os.path.dirname(args.critical_points_file), exist_ok=True)
            # Write to file
            with open(args.critical_points_file, "w") as file:
                file.write(f"{points}")
        else:
            print(f"The 80% critical point is {points[0] * 100}% of the total core count\n" +
                  f"The 60% critical point is {points[1] * 100}% of the total core count\0", file=sys.stdout)
