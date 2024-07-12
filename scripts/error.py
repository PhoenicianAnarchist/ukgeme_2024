#!/usr/bin/env python3
import argparse
import pathlib
import json
from sys import exit

import _common

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
    tallied_votes, total_votes = _common.calc_tallied_votes(json_data)
    tallied_seats, total_seats = _common.calc_tallied_seats(json_data)
    tallied_error, total_error = calc_error(tallied_votes, tallied_seats)

    name_max_length = max(len(s) for s in tallied_error.keys())
    header_fmtstr = f"{{:<{name_max_length}}} | {{:>7}}"
    row_fmtstr = f"{{name:<{name_max_length}}} | {{error:>7.2%}}"
    hr = _common.build_hr((name_max_length, 7), ("<", ">"))

    tallied_error = {k: v for k, v in sorted(tallied_error.items())}

    print(header_fmtstr.format("Party Name", "Error"))
    print(hr)

    if args.sort == "name":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), reverse=args.reverse, key=lambda x: x[0]
            )
        }
    elif args.sort == "error":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), reverse=args.reverse, key=lambda x: x[1]
            )
        }

    for party, error in tallied_error.items():
        print(row_fmtstr.format(name=party, error=error))

    print(hr)
    print(row_fmtstr.format(name="Total Error", error=total_error))

def print_per_constituency(json_data, args):
    tallied_error = {}
    total_error = 0

    for name, data in json_data.items():
        tallied_votes, total_votes = tally_scorecard_votes(data["scorecards"])
        tallied_seats, total_seats = tally_scorecard_seats(data["scorecards"])
        _, constituency_error = calc_error(tallied_votes, tallied_seats)

        tallied_error[name] = constituency_error
        total_error += constituency_error

    name_max_length = max(len(s) for s in tallied_error.keys())
    header_fmtstr = f"{{:<{name_max_length}}} | {{:>7}}"
    row_fmtstr = f"{{name:<{name_max_length}}} | {{error:>7.2%}}"
    hr = _common.build_hr((name_max_length, 7), ("<", ">"))

    tallied_error = {k: v for k, v in sorted(tallied_error.items())}

    print(header_fmtstr.format("Constituency", "Error"))
    print(hr)

    if args.sort == "name":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), reverse=args.reverse, key=lambda x: x[0]
            )
        }
    elif args.sort == "error":
        tallied_error = {
            k: v for k, v in sorted(
                tallied_error.items(), reverse=args.reverse, key=lambda x: x[1]
            )
        }

    for party, error in tallied_error.items():
        print(row_fmtstr.format(name=party, error=error))

    print(hr)
    print(row_fmtstr.format(name="Average Error", error=(total_error/650)))

## Argument Parser ############################################################
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=["name", "error"], default="name")
parser.add_argument("-r", "--reverse", action="store_true")
parser.add_argument(
    "-c", "--constituency", action="store_true",
    help="Show error per constituency instead of overall error"
)

args = parser.parse_args()

## Load Data ##################################################################
json_data_path = pathlib.Path("./data/bbc2024.json")
with open(json_data_path, "r") as f:
    json_data = json.load(f)

## Main #######################################################################
if not args.constituency:
    print_overall_error(json_data, args)
    exit(0)

print_per_constituency(json_data, args)
