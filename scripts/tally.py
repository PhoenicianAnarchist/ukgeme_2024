#!/usr/bin/env python3
import argparse
import json

import _common
import _paths

class MergedParty:
    party_1: str
    party_2: str
    new_name: str

    def __init__(self, s):
        self.party_1, self.party_2, self.new_name = s.split(",")

    def __str__(self):
        return " ".join((self.party_1, "+", self.party_2, "=", self.new_name))

def get_party_from_scorecards(scorecards, party):
    for scorecard in scorecards:
        if scorecard["party"] == party:
            return scorecard

    return None

def merge_parties(json_data, args):
    for constituency, data in json_data.items():
        scorecards = data["scorecards"]
        for group in args.groups:
            p1 = get_party_from_scorecards(scorecards, group.party_1)
            if p1 is None:
                continue

            p2 = get_party_from_scorecards(scorecards, group.party_2)
            if p2 is None:
                continue

            new_scorecard = {
                "candidate": "N/A",
                "party": group.new_name,
                "vote_count": p1["vote_count"] + p2["vote_count"]
            }

            scorecards = [x for x in scorecards if x["party"] != group.party_1]
            scorecards = [x for x in scorecards if x["party"] != group.party_2]
            scorecards.append(new_scorecard)

            json_data[constituency]["scorecards"] = scorecards

    return json_data

def print_overall_tally(json_data, args):
    tallied_votes, total_votes = _common.calc_tallied_votes(json_data)
    tallied_seats, total_seats = _common.calc_tallied_seats(json_data)

    headers = ("Party Name", "Votes", "Seats", "Votes/Seat")
    max_lengths = (
        _common.get_max_column_width(headers[0], tallied_votes.keys()),
        _common.get_max_column_width(
            headers[1], (str(x["vote_count"]) for x in tallied_votes.values())
        ),
        _common.get_max_column_width(
            headers[2], (str(x["seat_count"]) for x in tallied_seats.values())
        ),
        len(headers[3]) # good enough
    )

    header_fmtstr = _common.build_row_fmtstr(max_lengths, ("<", "<", "<", "<"))
    row_fmtstr    = _common.build_row_fmtstr(max_lengths, ("<", ">", ">", ">"))
    hr_str        = _common.build_hr_str(    max_lengths, ("<", ">", ">", ">"))

    tallies = {}
    for party, votes in tallied_votes.items():
        votes = votes["vote_count"]
        seats = 0
        vps = "N/A"
        try:
            seats = tallied_seats[party]["seat_count"]
            vps = int(votes / seats)
        except KeyError:
            if (args.ignore_zero):
                continue

            pass

        tallies[party] = (votes, seats, vps)

    print(header_fmtstr.format(*headers))
    print(hr_str)

    if args.sort == "name":
        tallies = {
            k: v for k, v in sorted(
                tallies.items(), reverse=args.reverse,
                key=lambda x: x[0]
            )
        }
    elif args.sort == "votes":
        tallies = {
            k: v for k, v in sorted(
                tallies.items(), reverse=not args.reverse,
                key=lambda x: x[1][0]
            )
        }
    elif args.sort == "seats":
        tallies = {
            k: v for k, v in sorted(
                tallies.items(), reverse=not args.reverse,
                key=lambda x: x[1][1]
            )
        }
    elif args.sort == "vps":
        tallies = {
            k: v for k, v in sorted(
                tallies.items(), reverse=not args.reverse,
                key=lambda x: x[1][2] if x[1][2] != "N/A" else 0
            )
        }

    for party, (votes, seats, vps) in tallies.items():
        print(row_fmtstr.format(party, votes, seats, vps))

## Argument Parser ############################################################
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--sort", choices=["name", "votes", "seats", "vps"], default="name"
)
parser.add_argument("-r", "--reverse", action="store_true")
parser.add_argument(
    "-z", "--ignore-zero", action="store_true",
    help="Ignore parties with zero seats"
)
parser.add_argument(
    "-g", "--groups", type=MergedParty, action="append",
    help="any number of groupings in the form of `<Party1>,<Party2>,<NewName>`"
)
parser.add_argument(
    "-c", "--constituency", nargs="?",
    help="show results for a single constituency, useful with --groups"
)

args = parser.parse_args()

## Load Data ##################################################################
with open(_paths.json_data_path, "r") as f:
    json_data = json.load(f)

## Main #######################################################################
if args.groups is not None:
    json_data = merge_parties(json_data, args)

if args.constituency is None:
    print_overall_tally(json_data, args)
else:
    print_overall_tally(
        {args.constituency: json_data[args.constituency]},
        args
    )
