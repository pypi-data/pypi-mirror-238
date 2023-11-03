# USATT

Python tools for working with the USA Table Tennis (USATT) website. As far as I am aware, there is no official API
for the USATT site. So this works purely via grabbing the HTML pages from the site and parsing

# Simple CLI examples

To get the USATT ratings for a few USATT ids, using a few of the top ranked USATT ids as an example:

```shell
usatt ratings -i 1165420 220283 31126
```

gives

|   USATT# | Name       |   Tournament Rating |   Highest Tournament Rating |   Tournaments Played |   League Rating |   Highest League Rating |   Leagues Played |
|---------:|:-----------|--------------------:|----------------------------:|---------------------:|----------------:|------------------------:|-----------------:|
|  1165420 | Lei Kou    |                2790 |                        2864 |                   33 |            2816 |                    2843 |                3 |
|   220283 | Jinbao Ma  |                2760 |                        2809 |                   32 |            2723 |                    2723 |                5 |
|    31126 | Lily Zhang |                2600 |                        2641 |                   95 |            2446 |                    2483 |               41 |

To get a summary of all USATT ratings,

```shell
usatt summary --outfile usatt.csv
```

This  will dump all USATT ratings to a CSV file.
