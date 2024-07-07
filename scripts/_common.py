def calc_tallied_votes(json_data):
    """Tally total votes (popular vote)"""
    tallied_votes = {}
    total_votes = 0

    for constituency, results in json_data.items():
        for scorecard in results["scorecards"]:
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

def get_elected_party(scorecards):
    """Return party name with highest vote count"""
    party = ""

    # scorecards should be in order of highest votes to lowest, check anyway
    count = 0
    for scorecard in scorecards:
        if scorecard["vote_count"] <= count:
            continue

        party = scorecard["party"]
        count = scorecard["vote_count"]

    return party

def calc_tallied_seats(json_data):
    """Tally seats won by each party"""
    tallied_seats = {}
    total_seats = 0

    for constituency, results in json_data.items():
        party = get_elected_party(results["scorecards"])

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

def build_hr(widths, alignments):
    hr_str = ""
    last_col = len(widths) - 1

    for i, w in enumerate(widths):
        adj = 0;
        if i == 0 or i == last_col:
            adj = 1

        if alignments[i] == "<":
            hr_str += ":"
        else:
            hr_str += "-"

        hr_str += "-" * (w - adj)

        if alignments[i] == ">":
            hr_str += ":"
        else:
            hr_str += "-"

        if i != last_col:
            hr_str += "|"

    return hr_str
