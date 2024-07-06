#!/usr/bin/env python3
import argparse
import pathlib
import json

def parse_row_data(results):
    row_data = {}
    row_data["Constituency"] = results["meta"]["name"]
    row_data["Registered"] = results["meta"]["registered"]
    row_data["Turnout"] = results["meta"]["turnout"]

    # scorecards should be in order of highest votes to lowest, check anyway
    row_data["Vote Count"] = 0
    for scorecard in results["scorecards"]:
        if scorecard["vote_count"] <= row_data["Vote Count"]:
            continue

        row_data["Party"] = scorecard["party"]
        row_data["Candidate"] = scorecard["candidate"]
        row_data["Vote Count"] = scorecard["vote_count"]
        row_data["Vote Share"] = (
            row_data["Vote Count"] / results["meta"]["vote_count"]
        )

    row_data["Turnout"] = f'{row_data["Turnout"]:4.1%}'
    row_data["Vote Share"] = f'{row_data["Vote Share"]:4.1%}'

    return row_data

def make_hr_string(column_widths, column_types):
    hr_str = ""

    for i, w in column_widths.items():
        align = "<"
        if column_types[i] == type(1) or column_types[i] == type(1.0):
            align = ">"

        if align == "<":
            hr_str += ":"
        else:
            hr_str += "-"

        adjust = 0
        if (i == 0) or (i == len(column_widths) - 1):
            adjust = 1

        hr_str += "-" * (w - adjust)

        if align == ">":
            hr_str += ":"
        else:
            hr_str += "-"

        if i != (len(column_widths) - 1):
            hr_str += "|"

    return hr_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--sort", choices=["name", "turnout", "share"], default="name"
    )
    parser.add_argument("-r", "--reverse", action="store_true")

    args = parser.parse_args()

    json_data_path = pathlib.Path("./data/bbc2024.json")

    with open(json_data_path, "r") as f:
        json_data = json.load(f)

    rows = []
    column_headers = {}
    column_widths = {}
    column_types = {}

    # column header widths
    for constituency, results in json_data.items():
        row_data = parse_row_data(results)
        for i, (k, v) in enumerate(row_data.items()):
            column_widths[i] = len(k)
            column_headers[i] = k
            column_types[i] = type(v)
        break

    # column data widths
    for constituency, results in json_data.items():
        row_data = parse_row_data(results)
        rows.append(row_data)

        for i, (_, v) in enumerate(row_data.items()):
            w = len(str(v))

            if w > column_widths.get(i, 0):
                column_widths[i] = w

    header_fmtstr = ""
    hr_str = make_hr_string(column_widths, column_types)
    row_fmtstr = ""
    for i, w in column_widths.items():
        header_fmtstr += f"{{{i}:<{w}}}"
        if i != (len(column_widths) - 1):
            header_fmtstr += " | "

        align = "<"
        if column_types[i] == type(1) or column_types[i] == type(1.0):
            align = ">"

        row_fmtstr += f"{{{i}:{align}{w}}}"
        if i != (len(column_widths) - 1):
            row_fmtstr += " | "

    print(header_fmtstr.format(*column_headers.values()))
    print(hr_str)

    if args.sort == "name":
        rows = sorted(
            rows, key=lambda x: x["Constituency"], reverse=args.reverse
        )
    elif args.sort == "turnout":
        rows = sorted(
            rows, key=lambda x: x["Turnout"], reverse=args.reverse
        )
    elif args.sort == "share":
        rows = sorted(
            rows, key=lambda x: x["Vote Share"], reverse=args.reverse
        )

    for row in rows:
        print(row_fmtstr.format(*row.values()))
