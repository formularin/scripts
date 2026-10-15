#!/usr/bin/env python3
"""Gaussian (q-)binomial coefficients.

The Gaussian binomial coefficient [n, k]_q is the q-analogue of the ordinary
binomial coefficient; it reduces to C(n, k) when q = 1.  Running this file from
the command line prints the sum of [n, k]_q for k = 0 .. n (the Galois number
G_n when q is a prime power).
"""

import argparse
import sys


def gaussian_row(n, q):
    """Return [[n, 0]_q, [n, 1]_q, ..., [n, n]_q].

    Uses the Pascal-style recurrence

        [n, k]_q = [n-1, k-1]_q + q**k * [n-1, k]_q

    which keeps integer q exact (no division) and works for q = 1 as well.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    row = [1]
    for m in range(1, n + 1):
        nxt = [1] * (m + 1)
        for k in range(1, m):
            nxt[k] = row[k - 1] + q**k * row[k]
        row = nxt
    return row


def gaussian_coefficient(n, k, q):
    """Return the Gaussian binomial coefficient [n, k]_q."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return 0
    return gaussian_row(n, q)[k]


def gaussian_sum(n, q):
    """Return sum of [n, k]_q for k = 0 .. n."""
    return sum(gaussian_row(n, q))


def _parse_q(text):
    try:
        return int(text)
    except ValueError:
        return float(text)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sum the Gaussian binomial coefficients [n, k]_q for k = 0..n."
    )
    parser.add_argument("n", type=int, help="upper index (non-negative integer)")
    parser.add_argument("q", type=_parse_q, help="the q parameter (int or float)")
    parser.add_argument(
        "-t", "--terms", action="store_true", help="also print each [n, k]_q"
    )
    args = parser.parse_args(argv)

    if args.n < 0:
        parser.error("n must be non-negative")

    row = gaussian_row(args.n, args.q)
    if args.terms:
        for k, value in enumerate(row):
            print(f"[{args.n}, {k}]_{args.q} = {value}")
    print(sum(row))
    return 0


if __name__ == "__main__":
    print(gaussian_coefficient(2, 1, 2))
    # sys.exit(main())
