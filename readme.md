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

---

Inspired by an old [CGP Grey video][].

[BBC page]: <https://www.bbc.co.uk/news/election/2024/uk/constituencies>
[CGP Grey video]: <https://www.youtube.com/watch?v=r9rGX91rq5I>
