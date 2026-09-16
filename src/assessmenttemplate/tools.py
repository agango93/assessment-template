import pandas as pd
import sys
import os
from io import StringIO


def read_input_table(args) -> pd.DataFrame:
    """
    Read table from stanadrd input, UNIX pipe or a file in CSV or Markdown format and parse into DataFrame.
    :param args: User provided arguments containing input file name and verbosity switch
    :return: Table as a Pandas DataFrame
    """
    lines = []

    is_pipe = False

    if args.input:
        with open(args.input, 'r') as input_table:
            # Ref: https://stackoverflow.com/questions/15233340/getting-rid-of-n-when-using-readlines
            lines = input_table.read().splitlines()
    else:
        is_pipe = not os.isatty(sys.stdin.fileno())

        if not is_pipe:
            print(f"Please paste the data below, ending with an empty line:")

        for line in sys.stdin:
            if line.strip() == '':
                break
            lines.append(line)

    if (args.input or is_pipe) and args.verbose:
        print("Inputted table:")
        print("\n".join(lines))

    # Check that the separator exists, implying a Markdown table
    if '|' in lines[0]:
        print("Assuming Markdown table input, discarding two header rows")
        # Remove heading line
        del lines[1]
        lines = [line.strip('|').replace("|", ',') for line in lines]
    else:
        print("Assuming CSV input")

    table = pd.read_csv(StringIO("\n".join(lines)))

    # Drop any extra data
    table = table.drop(table.columns[2:], axis=1)

    return table
