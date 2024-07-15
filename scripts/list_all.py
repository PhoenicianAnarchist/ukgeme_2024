#!/usr/bin/env python3
import argparse
import json

import _common
import _paths

def parse_row_data(constituency_results):
    # scorecards should be in order of highest votes to lowest, check anyway
    scorecard = sorted(
        constituency_results["scorecards"],
        key=lambda x: x["vote_count"],
        reverse=True
    )[0]

    row_data = (
        constituency_results["meta"]["name"],
        constituency_results["meta"]["registered"],
        constituency_results["meta"]["turnout"],
        scorecard["party"],
        scorecard["candidate"],
        scorecard["vote_count"],
        scorecard["vote_count"] / constituency_results["meta"]["vote_count"]
    )

    return row_data

def print_table(json_data, args):
    rows = []

    column_headers = (
        "Constituency",
        "Registered",
        "Turnout",
        "Party",
        "Candidate",
        "Vote Count",
        "Vote Share"
    )

    rows = []
    for constituency, results in json_data.items():
        row_data = parse_row_data(results)
        rows.append(row_data)

    max_lengths = (
        max(len(column_headers[0]), max(len(x[0]) for x in rows)),
        max(len(column_headers[1]), max(len(str(x[1])) for x in rows)),
        max(len(column_headers[2]), 7),
        max(len(column_headers[3]), max(len(x[3]) for x in rows)),
        max(len(column_headers[4]), max(len(x[4]) for x in rows)),
        max(len(column_headers[5]), max(len(str(x[5])) for x in rows)),
        max(len(column_headers[6]), 7)
    )


    header_fmtstr = _common.build_row_fmtstr(
        max_lengths,
        ("<", "<", "<", "<", "<", "<", "<")
    )
    row_fmtstr = _common.build_row_fmtstr(
        max_lengths,
        ("<", ">", ">", "<", "<", ">", ">"),
        ("", "", ".2%", "", "", "", ".2%")
    )
    hr_str = _common.build_hr_str(
        max_lengths,
        ("<", ">", ">", "<", "<", ">", ">")
    )

    print(header_fmtstr.format(*column_headers))
    print(hr_str)

    if args.sort == "party":
        rows = sorted(
            rows, key=lambda x: x[0], reverse=args.reverse
        )
    elif args.sort == "turnout":
        rows = sorted(
            rows, key=lambda x: x[2], reverse=not args.reverse
        )
    elif args.sort == "share":
        rows = sorted(
            rows, key=lambda x: x[6], reverse=not args.reverse
        )

    for row in rows:
        print(row_fmtstr.format(*row))

## Argument Parser ############################################################
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--sort", choices=["party", "turnout", "share"], default="party"
)
parser.add_argument("-r", "--reverse", action="store_true")
parser.add_argument(
    "-c", "--constituency", nargs="?",
    help="show results for a single constituency"
)
args = parser.parse_args()

## Load Data ##################################################################
with open(_paths.json_data_path, "r") as f:
    json_data = json.load(f)


## Main #######################################################################
if args.constituency is None:
    print_table(json_data, args)
else:
    print_table(
        {args.constituency: json_data[args.constituency]},
        args
    )
