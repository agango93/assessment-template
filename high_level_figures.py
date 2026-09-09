import argparse as ap
import assessmenttemplate.intranode as intranode
import assessmenttemplate.summary as summary


def _main():
    parser = ap.ArgumentParser(
        prog="high_level-graphs.py",
        description="Tools to generate plots for the high-level assessment.",
        epilog="Unless an output flag is specified, a requested output will be echoed to the standard console output."
    )

    # Source - https://stackoverflow.com/a/75100875
    # Posted by sinoroc, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-09-07, License - CC BY-SA 4.0

    import importlib.metadata
    version = importlib.metadata.version('assessmenttemplate')

    parser.add_argument("--version",
                        action="version",
                        version=f"%(prog)s {version}",
                        help="Show program version number and exit.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print extra debug outputs.")
    parser.add_argument("-d", "--default", action="store_true",
                        help="Output any requested outputs with unspecified file to their default file.")
    parser.add_argument("--svg", action="store_true",
                        help="Output graph to default file will output SVG rather than PNG.")
    parser.add_argument("-i", "--input",
                        default=None,
                        required=False,
                        help="Specify an optional input file containing the table for the metric."
                             "requested. Will use stdin if none specified.")
    parser.add_argument("-o", "--output",
                        help="Specify an output file. This can only be used if exactly one output type is requested.")
    parser.add_argument("-s", "--stdout-graph", action="store_true",
                        help="Output image data to stdout (useful for piping)")
    parser.add_argument("--show", action="store_true",
                        help="Show graph in window at runtime.")

    sub_parsers = parser.add_subparsers(dest="metric", required=True, help="Metric for which plots are to be "
                                                                           "generated.")
    # Add plots per mode
    intranode.intranode_add_args(sub_parsers)
    summary.summary_add_args(sub_parsers)

    args = parser.parse_args()

    if args.metric == "intranode":
        intranode.intranode_main(args)
    elif args.metric == "summary":
        summary.summary_main(args)


if __name__ == "__main__":
    _main()
