"""Script to get the USATT ratings based on USATT#s."""
from __future__ import annotations

import argparse
import warnings

import pandas as pd

from usatt._data import get_ratings, get_summary

warnings.simplefilter("ignore")


def run_get_ratings(args):
    """
    Get detailed usatt stats for a few users.
    :param args: Input args.
    """
    data = []

    for usattid in args.ids:
        data.append(get_ratings(usattid))

    df = pd.DataFrame(data)
    df = df.set_index("USATT#")
    print(df.to_markdown())


def run_get_summary(args):
    """
    Get summary USATT stats.
    :param args: Input args.
    """
    filter_ = None
    if args.filter is not None:
        filter_ = dict([k.split("=") for k in args.filter])

    all_data = get_summary(query=args.criteria, filter=filter_)

    if args.outfile:
        all_data.to_csv(args.outfile)
    else:
        print(all_data.to_markdown())


def main():
    """Handle main."""
    parser = argparse.ArgumentParser(
        description="""Use "usatt -h" to see options.""",
        epilog="""Author: Shyue Ping Ong""",
    )

    subparsers = parser.add_subparsers()

    p_ratings = subparsers.add_parser("ratings", help="Get the USATT ratings.")

    p_ratings.add_argument(
        "-i",
        "--ids",
        dest="ids",
        nargs="+",
        required=True,
        help="USATT ids to look for.",
    )
    p_ratings.set_defaults(func=run_get_ratings)

    p_summary = subparsers.add_parser("summary", help="Get a summary of USATT ratings based on a search.")

    p_summary.add_argument(
        "-c",
        "--criteria",
        dest="criteria",
        nargs="+",
        default=None,
        help="Query criteria",
    )
    p_summary.add_argument(
        "-f",
        "--filter",
        dest="filter",
        nargs="*",
        default=None,
        help="Filter criteria. E.g., minAge=18",
    )
    p_summary.add_argument(
        "-o",
        "--outfile",
        dest="outfile",
        default=None,
        help="Output filename. If not specified, it will be printed to stdout.",
    )

    p_summary.set_defaults(func=run_get_summary)

    args = parser.parse_args()

    return args.func(args)


if __name__ == "__main__":
    main()
