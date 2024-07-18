#!/usr/bin/env python3
import argparse
import json

import _common
import _paths

def parse_row_data(constituency_results):
    # scorecards should be in order of highest votes to lowest, check anyway
    scorecards = sorted(
        constituency_results["scorecards"],
        key=lambda x: x["vote_count"],
        reverse=True
    )

    scorecard = scorecards[0]
    majority = scorecard["vote_count"] - scorecards[1]["vote_count"]
    row_data = [
        constituency_results["meta"]["name"],
        constituency_results["meta"]["registered"],
        constituency_results["meta"]["turnout"],
        scorecard["party"],
        scorecard["candidate"],
        scorecard["vote_count"],
        scorecard["vote_count"] / constituency_results["meta"]["vote_count"],
        majority
    ]

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
        "Vote Share",
        "Majority"
    )

    rows = []
    for constituency, results in json_data.items():
        row_data = parse_row_data(results)

        if (args.majority_percentage):
            row_data[7] = row_data[7] / (row_data[2] * row_data[1])

        rows.append(row_data)

    m_w = max(len(str(x[7])) for x in rows)
    if (args.majority_percentage):
        m_w = 7

    max_lengths = (
        max(len(column_headers[0]), max(len(x[0]) for x in rows)),
        max(len(column_headers[1]), max(len(str(x[1])) for x in rows)),
        max(len(column_headers[2]), 7),
        max(len(column_headers[3]), max(len(x[3]) for x in rows)),
        max(len(column_headers[4]), max(len(x[4]) for x in rows)),
        max(len(column_headers[5]), max(len(str(x[5])) for x in rows)),
        max(len(column_headers[6]), 7),
        max(len(column_headers[7]), m_w)
    )

    m_a = ""
    if (args.majority_percentage):
        m_a = ".2%"

    header_fmtstr = _common.build_row_fmtstr(
        max_lengths,
        ("<", "<", "<", "<", "<", "<", "<", "<")
    )
    row_fmtstr = _common.build_row_fmtstr(
        max_lengths,
        ("<", ">", ">", "<", "<", ">", ">", ">"),
        ("", "", ".2%", "", "", "", ".2%", m_a)
    )
    hr_str = _common.build_hr_str(
        max_lengths,
        ("<", ">", ">", "<", "<", ">", ">", ">")
    )

    print(header_fmtstr.format(*column_headers))
    print(hr_str)

    if args.sort == "name":
        rows = sorted(rows, key=lambda x: x[0], reverse=args.reverse)
    elif args.sort == "turnout":
        rows = sorted(rows, key=lambda x: x[2], reverse=not args.reverse)
    elif args.sort == "share":
        rows = sorted(rows, key=lambda x: x[6], reverse=not args.reverse)
    elif args.sort == "majority":
        rows = sorted(rows, key=lambda x: x[7], reverse=not args.reverse)

    for row in rows:
        print(row_fmtstr.format(*row))

## Argument Parser ############################################################
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--sort", choices=["name", "turnout", "share", "majority"],
    default="name"
)
parser.add_argument("-r", "--reverse", action="store_true")
parser.add_argument(
    "-c", "--constituency", nargs=1,
    help="show results for a single constituency"
)
parser.add_argument("-p", "--majority-percentage", action="store_true")
args = parser.parse_args()

## Load Data ##################################################################
with open(_paths.json_data_path, "r") as f:
    json_data = json.load(f)

## Main #######################################################################
if args.constituency is None:
    print_table(json_data, args)
else:
    print_table(
        {args.constituency[0]: json_data[args.constituency[0]]},
        args
    )
