#!/usr/bin/env python3
"""Proper definite integrals by the trapezoidal rule.

Approximates the integral of f from a to b by splitting [a, b] into strips of
width dx and summing the area of the trapezoid over each strip:

    integral ~ dx * (f(x0)/2 + f(x1) + ... + f(x_{n-1}) + f(xn)/2)

Running this file from the command line evaluates an expression in x, e.g.

    ./trapezoid.py 'x**2' 0 3
    ./trapezoid.py 'sin(x)' 0 pi --dx 1e-5
"""

import argparse
import math


def trapezoid(f, a, b, dx=1e-4):
    """Return the trapezoidal approximation of the integral of f from a to b.

    The strip width is adjusted down to the nearest value that divides
    b - a evenly, so the last strip never overshoots b.  Swapping the bounds
    negates the result, as with an exact integral.
    """
    if dx <= 0:
        raise ValueError("dx must be positive")
    if a == b:
        return 0.0

    sign = 1.0
    if a > b:
        a, b = b, a
        sign = -1.0

    n = max(1, math.ceil((b - a) / dx))
    h = (b - a) / n

    total = (f(a) + f(b)) / 2.0
    for i in range(1, n):
        total += f(a + i * h)
    return sign * total * h


def _parse_bound(text):
    """Evaluate a bound, allowing math names such as pi or e."""
    return _make_function(text)(0.0)


def _make_function(expression):
    """Compile an expression in x into a one-argument function."""
    names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    code = compile(expression, "<expression>", "eval")

    def f(x):
        return eval(code, {"__builtins__": {}}, dict(names, x=x))

    return f


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Integrate an expression in x over [a, b] by the trapezoidal rule."
    )
    parser.add_argument("expression", help="integrand in terms of x, e.g. 'x**2'")
    parser.add_argument("a", type=_parse_bound, help="lower bound")
    parser.add_argument("b", type=_parse_bound, help="upper bound")
    parser.add_argument(
        "--dx", type=float, default=1e-4, help="target strip width (default: 1e-4)"
    )
    args = parser.parse_args(argv)

    if args.dx <= 0:
        parser.error("dx must be positive")

    print(trapezoid(_make_function(args.expression), args.a, args.b, args.dx))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
