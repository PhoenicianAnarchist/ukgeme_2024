#!/usr/bin/env python3
import argparse
import json
from sys import exit

import _common
import _paths

def calc_error(tallied_votes, tallied_seats):
    """Caclulates misrepresentation error"""
    tallied_error = {}
    total_error = 0

    for party in tallied_votes.keys():
        vote_share = tallied_votes[party]["vote_share"]

        seat_share = 0
        try:
            seat_share = tallied_seats[party]["seat_share"]
        except KeyError:
            pass

        error = abs(seat_share - vote_share)

        if party not in tallied_error.keys():
            tallied_error[party] = 0

        tallied_error[party] += error
        total_error += error

    return tallied_error, total_error

def tally_scorecard_votes(scorecards):
    tallied_votes = {}
    total_votes = 0

    for scorecard in scorecards:
        if scorecard["party"] not in tallied_votes.keys():
            tallied_votes[scorecard["party"]] = {
                "vote_count": 0
            }

        count = scorecard["vote_count"]
        tallied_votes[scorecard["party"]]["vote_count"] += count
        total_votes += count

    for party in tallied_votes.keys():
        count = tallied_votes[party]["vote_count"]
        tallied_votes[party]["vote_share"] = count / total_votes

    return tallied_votes, total_votes

def tally_scorecard_seats(scorecards):
    tallied_seats = {}
    total_seats = 0

    party = _common.get_elected_party(scorecards)

    if party not in tallied_seats:
        tallied_seats[party] = {
            "seat_count": 0
        }

    tallied_seats[party]["seat_count"] += 1
    total_seats += 1

    for party in tallied_seats.keys():
        count = tallied_seats[party]["seat_count"]
        tallied_seats[party]["seat_share"] = count / total_seats

    return tallied_seats, total_seats

def print_overall_error(json_data, args):
    v, _ = _common.calc_tallied_votes(json_data)
    s, _ = _common.calc_tallied_seats(json_data)
    tallied_error, total_error = calc_error(v, s)

    print_error_x(tallied_error, total_error, "Party Name", "Total Error")

def print_per_constituency(json_data, args):
    tallied_error = {}
    total_error = 0

    for name, data in json_data.items():
        v, _ = tally_scorecard_votes(data["scorecards"])
        s, _ = tally_scorecard_seats(data["scorecards"])
        _, constituency_error = calc_error(v, s)

        tallied_error[name] = constituency_error
        total_error += constituency_error

    print_error_x(
        tallied_error, total_error, "Party Name", "Average Error", True
    )

def print_error_x(tallied_error, total_error, h, f, average_total=False):
    c1w = max(len(h), len(f))
    headers = (h, "Error")
    max_lengths = (
        max(c1w, _common.get_max_column_width("", tallied_error.keys())),
        max(len(headers[1]), 7)
    )

    header_fmtstr = _common.build_row_fmtstr(max_lengths, ("<", "<"))
    row_fmtstr    = _common.build_row_fmtstr(max_lengths, ("<", ">"), ("", ".2%"))
    hr_str        = _common.build_hr_str(    max_lengths, ("<", ">"))

    tallied_error = {k: v for k, v in sorted(tallied_error.items())}

    print(header_fmtstr.format(*headers))
    print(hr_str)

    if args.sort == "name":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), key=lambda x: x[0],
                reverse=args.reverse
            )
        }
    elif args.sort == "error":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), key=lambda x: x[1],
                reverse=not args.reverse
            )
        }

    for party, error in tallied_error.items():
        print(row_fmtstr.format(party, error))

    print(hr_str)

    if (average_total):
        print(row_fmtstr.format(f, total_error / len(tallied_error)))
    else:
        print(row_fmtstr.format(f, total_error))

## Argument Parser ############################################################
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=["name", "error"], default="name")
parser.add_argument("-r", "--reverse", action="store_true")
parser.add_argument(
    "-c", "--constituency", nargs="*",
    help="Show error per constituency instead of overall error"
)

args = parser.parse_args()

## Load Data ##################################################################
with open(_paths.json_data_path, "r") as f:
    json_data = json.load(f)

## Main #######################################################################
if args.constituency is None:
    print_overall_error(json_data, args)
elif len(args.constituency) == 0:
    print_per_constituency(json_data, args)
else:
    print_overall_error(
        {args.constituency[0]: json_data[args.constituency[0]]},
        args
    )
