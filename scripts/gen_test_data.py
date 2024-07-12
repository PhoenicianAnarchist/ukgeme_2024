#!/usr/bin/env python3
import json

import _paths

registered = 80000
turnout = 0.56
vote_count = int(registered * turnout)

data = {}
for i in range(326):
    name = f"Constituency {i:0>3}"
    data[name] = {
        "meta": {
            "name": name,
            "registered": registered,
            "turnout": turnout,
            "vote_count": vote_count
        },
        "scorecards": [
            {
                "candidate": "N/A",
                "party": "Red",
                "vote_count": int(vote_count * 0.30)
            },
            {
                "candidate": "N/A",
                "party": "Blue",
                "vote_count": int(vote_count * 0.29)
            },
            {
                "candidate": "N/A",
                "party": "Green",
                "vote_count": int(vote_count * 0.21)
            },
            {
                "candidate": "N/A",
                "party": "Yellow",
                "vote_count": int(vote_count * 0.20)
            }
        ]
    }

for i in range(324):
    name = f"Constituency {(i + 326):0>3}"
    data[name] = {
        "meta": {
            "name": name,
            "registered": registered,
            "turnout": turnout,
            "vote_count": vote_count
        },
        "scorecards": [
            {
                "candidate": "N/A",
                "party": "Red",
                "vote_count": int(vote_count * 0.20)
            },
            {
                "candidate": "N/A",
                "party": "Blue",
                "vote_count": int(vote_count * 0.29)
            },
            {
                "candidate": "N/A",
                "party": "Green",
                "vote_count": int(vote_count * 0.30)
            },
            {
                "candidate": "N/A",
                "party": "Yellow",
                "vote_count": int(vote_count * 0.21)
            }
        ]
    }

with open(_paths.json_data_path, "w") as f:
    json.dump(data, f, indent=2)
