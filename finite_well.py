"""Creates an interactive plot of energy eigenvalues (less than the potential) of a particle in a finite square well.

usage: python3 finite_well.py <potential> <size> <mass>

Arguments
---------
- potential: the depth of the well, in electron volts
- size: width of the well, in nanometers
- mass: mass of the particle, in eV/c^2
"""

import math
import sys

import matplotlib.pyplot as plt
import mplcursors
import numpy as np


H_BAR = 4.1356677e-15 / (2*math.pi)  # eV * s
C = 299792458  # m / s
EPS = 1e-9


def bisect(f, lo: float, hi: float) -> float:
    """Finds a root of an increasing function f in [lo, hi], given f(lo) <= 0 <= f(hi)."""
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def branches(z0: float, offset: float):
    """Yields the intervals [n*pi + offset, n*pi + offset + pi/2] (clipped to z0) that start below z0."""
    start = offset
    while start < z0:
        yield start, min(start + math.pi/2 - EPS, z0)
        start += math.pi


def make_plots(potential: float, size: float, mass: float):
    r"""Makes an interactive plot with two axes: one for energies corresponding to even eigenstates and one for energies corresponding to odd eigenstates.

    Let
    $$z=\sqrt(\frac{2mE_na^2}{\hbar^2})$$
    $$z_0=\sqrt(\frac{2mV_0a^2}{\hbar^2})$$

    The even plot shows $z\tan(z)$, and the odd plot shows $-z\cot(z)$.
    Both plots show $\sqrt{z_0^2-z^2}$.
    """
    a = size / 2 / 1e9  # the well spans [-a, a]
    z0 = a * math.sqrt(2 * mass * potential) / (H_BAR * C)

    def circle(z):
        return np.sqrt(np.maximum(z0**2 - z**2, 0))

    curves = {
        "Even": (0, r"$z\tan(z)$", lambda z: z * np.tan(z)),
        "Odd": (math.pi/2, r"$-z\cot(z)$", lambda z: -z / np.tan(z)),
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    energies = {}
    for ax, (parity, (offset, label, curve)) in zip(axes, curves.items()):
        roots = []
        for i, (lo, hi) in enumerate(branches(z0, offset)):
            z = np.linspace(lo, hi, 500)
            ax.plot(z, curve(z), color="C0", label=label if i == 0 else None)
            roots.append(bisect(lambda z: curve(z) - circle(z), lo, hi))

        z = np.linspace(0, z0, 500)
        ax.plot(z, circle(z), color="C1", label=r"$\sqrt{z_0^2-z^2}$")

        roots = np.array(roots)
        points = ax.scatter(roots, circle(roots), color="C3", zorder=3)
        energies[points] = (parity, potential * (roots / z0)**2)

        ax.set_title(f"{parity} eigenstates")
        ax.set_xlabel("$z$")
        ax.set_xlim(0, z0 * 1.05)
        ax.set_ylim(0, z0 * 1.5)
        ax.legend(loc="upper right")

    cursor = mplcursors.cursor(list(energies), hover=False)

    @cursor.connect("add")
    def on_add(sel):
        parity, values = energies[sel.artist]
        sel.annotation.set_text(f"{parity} state {sel.index + 1}\nE = {values[sel.index]:.6g} eV")

    fig.suptitle(f"Finite square well: $V_0$ = {potential:g} eV, width = {size:g} nm, $z_0$ = {z0:.4g}")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    potential = float(sys.argv[1])
    size = float(sys.argv[2])
    mass = float(sys.argv[3])
    make_plots(potential, size, mass)

