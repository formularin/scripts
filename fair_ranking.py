"""Takes a set of individual rankings and aggregates them into a "fair" ranking.

The fair ranking sorts elements lexicographically according to the following
keys:
 - the element's lowest rank among the individual rankings
 - the element's second-lowest rank among the individual rankings
 - etc.
 - the element's rank in dictionary order

Rankings are given as command-line arguments, where each ranking is a
comma-separated list of elements. Occurring sooner in the list
indicates a higher rank for an element.

Example:
```
$ python fair_ranking.py 1,2,3,4 4,3,2,1
2,3,1,4
```
"""

import sys


def _lex_key(indv_ranks: list[list], elem):
    """Computes the lexicographic sort key for an element, including
    the final "default" sorting criterion.
    """
    indices = [rank.index(elem) for rank in indv_ranks]
    return tuple(sorted(indices, reverse=True)) + (elem,)


def fair_ranking(indv_ranks: list[list]) -> list:
    """Aggregates a list of individual rankings.

    Args:
        indv_ranks: A list of lists, each of which contains the same
            set of comparable elements (and no duplicates).

    Returns:
        An aggregated ranking of the shared set of elements from
        `indv_ranks`.
    """
    return list(sorted(indv_ranks[0], key=lambda x: _lex_key(indv_ranks, x)))


if __name__ == "__main__":
    print(",".join(fair_ranking([rank.split(",") for rank in sys.argv[1:]])))

