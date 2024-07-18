---
layout: page
title: Splitting the Voter Base
---

One of the reasons that I chose to write these scripts is to examine the idea
of the "right wing" being split between `Conservative` and `Reform UK` being
the cause of `Labour`'s "victory".

Due to how the voting system works, this is not as simple as adding the number
of each seats for each party.

This can be tested with the command:

`./scripts/tally.py -z -s seats -g "Conservative, Reform UK, Conservative"`

Party Name                                     | Votes    | Seats | Votes/Seat
:----------------------------------------------|---------:|------:|----------:
Conservative                                   | 10933351 |   302 |      36203
Labour                                         |  9704655 |   267 |      36347
Liberal Democrat                               |  3519199 |    46 |      76504
... | ... | ... | ...

The 121 `Conservative` and 5 `Reform UK` seats could have been a potential 302
seats in this simplified example. This is the effect that splitting a voter
base has with the FPTP system.
