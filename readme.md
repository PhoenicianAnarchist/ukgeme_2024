# UK General Election Misrepresentation Error

An overview of misrepresentation error within the 2024 UK General Election, and
other related statistics (e..g the "right wing" voter base split between
`Conservative` and `Reform UK`).

Due to the changes in constituency boundaries, some data for changes since the
last election won't be included.

## ./scripts/fetch_bbc2024.py

This script will scrape the election data from the [BBC page][]. There is no
guarantee that this data will remain available for any length of time, or be
in a stable format, so this script _will_ stop working at some point.

## ./scripts/list_all.py

This script produces a (large) markdown formatted table showing elected
candidate, party, and voter turnout for each constituency.

The sorting order can be specified with the `-s` option. The choices for this
option are `name`, `turnout`, and `share`. The sorting direction can be
reversed with the `-r` flag.

## ./scripts/tally.py

This script generates a markdown formatted table tallying the number of seats
for each party.

The sorting order can be specified with the `-s` option. The choices for this
option are `party`, `seats`. The sorting direction can be reversed with the
`-r` flag.

### Splitting the Voter Base

One of the reasons that I chose to write these scripts is to examine the idea
of the "right wing" being split between `Conservative` and `Reform UK` being
the cause of `Labour`'s "victory".

Due to how the voting system works, this is not as simple as adding the number
of each seats for each party.

The `--groups` option can be given an arbitrary number of groupings in the
format of `<Party1>,<Party2>,<NewName>`, (e.g. `Conservative,Reform UK,REFCON`)
to automatically merge the vote count of the two parties in each constituency.

Data from a single constituency can be shown with the `--constituency` option.

---

Inspired by an old [CGP Grey video][].

[BBC page]: <https://www.bbc.co.uk/news/election/2024/uk/constituencies>
[CGP Grey video]: <https://www.youtube.com/watch?v=r9rGX91rq5I>
