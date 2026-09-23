#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys
import os
from enum import StrEnum, auto

import pandas as pd

from assessmenttemplate.tools import read_input_table


class Rubric(StrEnum):
    Core = auto()
    GPU = auto()
    IO = auto()
    INTRA = auto()
    INTER = auto()
    UNKNOWN = auto()


def from_string(from_str: str):
    match from_str.lower():
        case s if s.startswith(Rubric.Core):
            return Rubric.Core
        case s if s.startswith(Rubric.GPU):
            return Rubric.GPU
        case s if s.startswith(Rubric.IO):
            return Rubric.IO
        case s if s.startswith(Rubric.INTRA):
            return Rubric.INTRA
        case s if s.startswith(Rubric.INTER):
            return Rubric.INTER
        case _:
            return Rubric.UNKNOWN


def summary_to_spiderweb(table: pd.DataFrame) -> plt.Figure:
    """ 
    Create matplotlib spiderweb diagram

    :param table: Pandas DataFrame containing rubrics and the assigned 0-to-1-normalised score
    :return: matplotlib figure
    """

    nvars = len(table.index)
    angles = np.linspace(0, 2 * np.pi, nvars, endpoint=False).tolist()
    scores = table["Score"].to_numpy()
    scores = np.append(scores, scores[0])
    angles = np.append(angles, angles[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.fill(angles, scores, color='lightseagreen', alpha=0.4)  # Fill area
    ax.plot(angles, scores, color='teal', linewidth=2)  # Outline

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(table["Rubric"])

    for label in ax.get_xticklabels():
        label.set_weight('bold')

    ax.set_title("Rubric Scores", fontsize=14)

    return fig


def summary_to_bar_chart(table: pd.DataFrame) -> plt.Figure:
    """ 
    Create matplotlib bar chart

    :param table: Pandas DataFrame containing rubrics and the assigned 0-to-1-normalised score
    :return: matplotlib figure
    """

    fig, ax = plt.subplots()

    sns.barplot(data=table, x="Rubric", y="Score")
    ax.set_ylim(0.0, 1.0)

    # Rotate labels so they don't overlap
    fig.autofmt_xdate()

    plt.tight_layout()

    return fig


def summary_add_args(main_parser):
    parser = main_parser.add_parser("summary",
                                    description=f"Generate a spiderweb diagram or bar graph for the SHAREing "
                                                "high-level performance assessment." + summary_main.__doc__)

    parser.add_argument("-b", "--bar", action="store_true", help="Output a bar chart instead of a spiderweb.")


def summary_parse_args(unparsed_args):
    args = unparsed_args
    if args.verbose:
        print(f"args: {args}")

    if args.default and not args.output:
        args.output = f"images/summary.{"svg" if args.svg else "png"}"

        if args.verbose:
            print(f"STATUS: Setting output to default filepath:{args.output}")

    elif args.default and args.output:
        print("WARNING: Specifying output file overrides request to output to default file.")

    if args.svg and not args.default:
        print(
            "WARNING: svg flag only has an effect when outputting to the default file. "
            "Matplotlib will output to svg if you specify a filename with file ending '.svg'")

    return args


def summary_main(unparsed_args):
    """
    This script may be passed either a Markdown table containing thread count, time, and (optional) parallel efficiency,
    or by passing CSV thread count, time.

    It can output a matplotlib graph and a Markdown formatted table with all three columns filled in.
    """

    args = summary_parse_args(unparsed_args)

    ####################
    # INPUT PROCESSING #
    ####################

    if args.verbose:
        print("STATUS: processing input")

    table = read_input_table(args)

    # Rename columns incase alternative names used
    table.columns = ["Rubric", "Score"]

    #####################
    # OUTPUT GENERATION #
    #####################

    if args.verbose:
        print("STATUS: generating graph")

    if args.bar:
        fig = summary_to_bar_chart(table)
    else:
        fig = summary_to_spiderweb(table)
    if args.output:
        # Ensure output directory exists
        if '/' in args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
        # Save figure to file
        fig.savefig(args.output)
    if args.stdout_graph:
        fig.savefig(sys.stdout)
    if args.show:
        plt.show()
