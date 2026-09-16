import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import os

from assessmenttemplate.tools import read_input_table


def intranode_compute_metrics(table: pd.DataFrame, verbose=False):
    """
    Process input table and compute parallel efficiency per core count

    :param table: Pandas dataframe containing time taken in seconds per core count
    :param verbose: Verbose output if requested (and arguments are provided)
    """
    # Calculate speed-up and parallel efficiency
    serial_time = table.loc[table["Cores"] == 1, "Time"].iloc[0]
    table["Speed-up"] = serial_time / table["Time"]
    table["Efficiency"] = table["Speed-up"] / table["Cores"]

    if verbose:
        print(f"Calculated efficiencies")


def intranode_times_crit_80_60(table: pd.DataFrame, prop=False) -> tuple[float, float]:
    """
    Calculate the 80% and 60% critical points/proportions

    :param table: Pandas dataframe containing parallel efficiency per core count
    :param prop: Return porportional values instead of direct critical points
    :return: 80% proportion, 60% proportion
    """

    # Calculate 80%/60% critical core points

    p_crit_80 = table.loc[table["Efficiency"] >= 0.8, "Cores"].max()
    p_crit_60 = table.loc[table["Efficiency"] >= 0.6, "Cores"].max()

    if prop:
        intra_node_prop_80 = float(p_crit_80 / table["Cores"].max())
        intra_node_prop_60 = float(p_crit_60 / table["Cores"].max())
        return intra_node_prop_80, intra_node_prop_60

    return p_crit_80, p_crit_60


def intranode_times_to_graph(table: pd.DataFrame, critical_points=False, verbose=False) -> plt.Figure:
    """ 
    Create seaborn graph

    :param table: Pandas dataframe containing parallel efficiency per core count
    :param critical_points: Add critical points to the graph
    :param verbose: Verbose output if requested (and arguments are provided)
    :return: matplotlib figure
    """

    if verbose:
        print("Plotting graph")

    fig, ax = plt.subplots()
    ax.set_xlabel(r'$p$')
    ax.set_ylabel(r'$E(p)$')

    sns.lineplot(data=table, x="Cores", y="Efficiency", color="black", ax=ax)

    if critical_points:
        if verbose:
            print("Adding critical points to plot")
        p_crit_80, p_crit_60 = intranode_times_crit_80_60(table)
        ax.axvline(x=p_crit_80, color="#ffc844", linestyle="--")
        ax.text(p_crit_80, 0.05, "80%", rotation=90)
        ax.axvline(x=p_crit_60, color="#e35555", linestyle="--")
        ax.text(p_crit_60, 0.05, "60%", rotation=90)

    ax.set_title("Intra-node strong scaling efficiency", fontsize=14)

    return fig


def intranode_times_to_markdown(table: pd.DataFrame) -> str:
    """
    Generate Markdown table
    :param table: Pandas dataframe containing parallel efficiency per core count
    :return: String containing Markdown table
    """
    selection = {"Cores": "Core/thread count", "Time": "Time (s)", "Efficiency": "Parallel efficiency"}
    return table[list(selection.keys())].rename(columns=selection).to_markdown(index=False)


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

    table = read_input_table(args)

    ####################
    # INPUT PROCESSING #
    ####################

    if args.verbose:
        print("STATUS: processing input")

    # Rename columns incase alternative names used
    table.columns = ["Cores", "Time"]

    intranode_compute_metrics(table, verbose=args and args.verbose)

    #####################
    # OUTPUT GENERATION #
    #####################

    if args.graph:
        if args.verbose:
            print("STATUS: generating graph")
        fig = intranode_times_to_graph(table, critical_points=args and args.critical_points,
                                       verbose=args and args.verbose)
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
        table_md = intranode_times_to_markdown(table)
        if args.markdown_file:
            # Ensure output directory exists
            if '/' in args.markdown_file:
                os.makedirs(os.path.dirname(args.markdown_file), exist_ok=True)
            # Write to file
            with open(args.markdown_file, "w") as file:
                file.write(f"{table_md}")
        else:
            print(f"{table_md}\0")

    if args.critical_points:
        if args.verbose:
            print("STATUS: calculating critical points")
        points = intranode_times_crit_80_60(table, prop=True)
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
