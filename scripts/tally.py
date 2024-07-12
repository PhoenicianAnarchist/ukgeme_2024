#!/usr/bin/env python3
import argparse
import pathlib
import json

import _common

def print_overall_tally(json_data, args):
    tallied_votes, total_votes = _common.calc_tallied_votes(json_data)
    tallied_seats, total_seats = _common.calc_tallied_seats(json_data)

    name_max_length = max(len(s) for s in tallied_votes.keys())
    header_fmtstr = f"{{:<{name_max_length}}} | {{:>7}} | {{:>5}} | {{:>10}}"
    row_fmtstr = f"{{name:<{name_max_length}}} | {{votes:>7}} | {{seats:>5}} | {{vps:>10}}"
    hr = _common.build_hr((name_max_length, 7, 5, 10), ("<", ">", ">", ">"))

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

    print(header_fmtstr.format("Party Name", "Votes", "Seats", "Votes/Seat"))
    print(hr)

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
        print(row_fmtstr.format(name=party, votes=votes, seats=seats, vps=vps))


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

args = parser.parse_args()

## Load Data ##################################################################
json_data_path = pathlib.Path("./data/bbc2024.json")
with open(json_data_path, "r") as f:
    json_data = json.load(f)

## Main #######################################################################
print_overall_tally(json_data, args)
exit(0)
