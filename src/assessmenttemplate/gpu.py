import sys
import pandas as pd

from assessmenttemplate.tools import read_input_table


def gpu_read_metric_table(args) -> pd.DataFrame:
    """
    Read in the metrics from Nsight Compute from standard input, UNIX pipe or a file in CSV format,
    parse into a DataFrame, filter for relevant metrics, and compute total number of operations.

    :param args: User provided arguments containing input file name and verbosity switch
    :return: Table as a Pandas DataFrame
    """

    # Create list of metrics to be filtered from the overall CSV and assign the weight for those operations
    metric_names = [f"sm__sass_thread_inst_executed_op_fp{metric}_pred_on.sum" for metric in ["16", "32", "64"]]
    metrics = read_input_table(args)

    # Isolate metrics and their values
    metrics = metrics[["Metric Name", "Metric Value"]]

    metrics = metrics.rename(columns={"Metric Name": "Metric", "Metric Value": "# operations"})

    # Filter for relevant metrics
    # Ref: https://stackoverflow.com/questions/19960077/how-to-filter-pandas-dataframe-using-in-and-not-in-like-in-sql
    metrics = metrics[metrics["Metric"].isin(metric_names)]

    # Remove any thousand separator commas
    metrics["# operations"] = metrics["# operations"].apply(lambda x: x.replace(',', ''))
    # Convert number of operations to ints
    metrics["# operations"] = metrics["# operations"].astype(int)

    # Sum-up operations per metric across all kernel calls
    metrics = metrics.groupby(by=["Metric"], dropna=True).sum().reset_index()

    metrics["Metric"] = metrics["Metric"].apply(lambda x: f"`{x}`")

    # Add the total number of operations at the end of the table
    metrics.loc[len(metrics)] = ["Total", metrics["# operations"].sum()]

    return metrics


def gpu_add_args(main_parser):
    """
    Add the sub-parser for the gpu mode. No further arguments are required

    :param main_parser: Main parser to which the modes will be added as subparsers
    """
    main_parser.add_parser("gpu",
                           description="Compute the GPU score from the metrics collected from Nsight Compute for the "
                                       "SHAREing high-level performance assessment.")


def gpu_parse_args(unprocessed_args):
    """
    Further process arguments for the gpu mode

    :param unprocessed_args: Arguments from the parser to be further processed for the "gpu" mode

    :return: Final processed arguments for "summary"
    """
    args = unprocessed_args
    if args.verbose:
        print(f"args: {args}")

    if args.default and not args.output:
        args.output = "gpu_metrics.md"

        if args.verbose:
            print(f"STATUS: Setting output to default filepath:{args.output}")

    elif args.default and args.output:
        print("WARNING: Specifying output file overrides request to output to default file.")

    return args


def gpu_main(unprocessed_args):
    """
    Processes parsed commandline arguments and the input CSV table containing GPU metrics from Nsight Compute.

    Filters for relevant metrics, computes the total number of operations on the GPU and outputs the metrics in
    Markdown format.

    :param unprocessed_args: Arguments from the parser to be further processed for the selected mode
    """

    args = gpu_parse_args(unprocessed_args)

    if args.verbose:
        print(f"args: {args}")

    ####################
    # INPUT PROCESSING #
    ####################

    if args.verbose:
        print("STATUS: processing input")

    table = gpu_read_metric_table(args)

    if args.output:
        writer = sys.stdout if args.output == "stdout" else open(args.output, "w")
        print(table.to_markdown(index=False), file=writer)
        writer.close()
