#!/usr/bin/env python3
import argparse
import pathlib
import json

def get_elected_party(results):
    party = ""

    # scorecards should be in order of highest votes to lowest, check anyway
    count = 0
    for scorecard in results["scorecards"]:
        if scorecard["vote_count"] <= count:
            continue

        party = scorecard["party"]
        count = scorecard["vote_count"]

    return party

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--sort", choices=["party", "seats"], default="party"
    )
    parser.add_argument("-r", "--reverse", action="store_true")

    args = parser.parse_args()

    json_data_path = pathlib.Path("./data/bbc2024.json")

    with open(json_data_path, "r") as f:
        json_data = json.load(f)

    max_width = 0
    parties = {}
    for constituency, results in json_data.items():
        party = get_elected_party(results)

        if party not in parties:
            w = len(party)
            if w > max_width:
                max_width = w

            parties[party] = 0

        parties[party] += 1

    if args.sort == "party":
        parties = {
            k: v for k, v in sorted(
                parties.items(), reverse=args.reverse, key=lambda x: x[0]
            )
        }
    elif args.sort == "seats":
        parties = {
            k: v for k, v in sorted(
                parties.items(), reverse=args.reverse, key=lambda x: x[1]
            )
        }

    print("{:<{w}} | {:>5}".format("Party", "Seats", w = max_width))
    print(":{:-<{w}}-|-{:->4}:".format("-", "-", w = (max_width - 1)))
    for party, seats in parties.items():
        print(f"{party:<{max_width}} | {seats:>5}")
