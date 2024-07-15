# UK General Election Misrepresentation Error

An overview of misrepresentation error within the 2024 UK General Election, and
other related statistics (e..g the "right wing" voter base split between
`Conservative` and `Reform UK`).

Due to the changes in constituency boundaries, some data for changes since the
last election won't be included.

## Getting The Data

### ./scripts/fetch_bbc2024.py

This script will scrape the election data from the [BBC page][]. There is no
guarantee that this data will remain available for any length of time, or be
in a stable format, so this script will most likely stop working at some point.

### ./scripts/get_test_data.py

In order to explore the extent to which our voting system is broken, this
script will generate some synthetic voting data where the opposition has a
higher share of the popular vote. This data also features a third party which
has the highest voter share, yet not a single seat.

## Python Scripts

### Common Options

Each script shares some common options:

- `-h`, `--help`
: shows all options and usage for the given script

- `-s`, `--sort`
: specify the column to use for sorting, defaults to `name`, (either the party
  name, or constituency name, depending on other options).

- `-r`, `--reverse`
: reverse the sorting order, default for text is A-Z, default for numbers is
  descending.

- `-c`, `--constituency`
: Specify a constituency to examine instead of outputting overall data.

### ./scripts/error.py

This script calculates the overall misrepresentation error.

Sorting options:

- `name`
- `error`

Other options:

- `-c`, `--constituency`
: This option can also be specified on its own (without a constituency) to
  output data for all constituencies.

### ./scripts/list_all.py

This script produces a (large) markdown formatted table showing elected
candidate, party, and voter turnout for each constituency.

Sorting options:

- `name`
- `turnout`
- `share`

### ./scripts/tally.py

This script generates a markdown formatted table tallying the number of seats
for each party.

Sorting options:

- `name`
- `votes`
- `seats`
- `vps` (votes per share)

Other options:

- `-z`, `--ignore-zero`
: Don't output data for parties with zero seats.

- `-g`, `--groups`
: Groups the votes for two parties as if they were one, and renames it. e.g.
`-g "Party One, Party Two, New Party"` will group `Party One` and `Party Two`
votes under the name `New Party`.

#### Splitting the Voter Base

One of the reasons that I chose to write these scripts is to examine the idea
of the "right wing" being split between `Conservative` and `Reform UK` being
the cause of `Labour`'s "victory".

Due to how the voting system works, this is not as simple as adding the number
of each seats for each party.

---

Inspired by an old [CGP Grey video][].

[BBC page]: <https://www.bbc.co.uk/news/election/2024/uk/constituencies>
[CGP Grey video]: <https://www.youtube.com/watch?v=r9rGX91rq5I>
