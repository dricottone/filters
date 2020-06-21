#!/usr/bin/env python3

"""rng normal [OPTIONS]
Uniform distribution - Generate random data from a normal distribution.

Options:
  -d, --delta   velocity of average per time unit [Default: 0]
  -m, --mu      average of distribution [Default: 0]
  -n, --number  number of random data points to generate [Default: 10]
  -s, --sigma   standard deviation of distribution [Default: 1]

Currently assumed that sigma is constant over time.
"""

import sys
import random
import itertools
from typing import Callable, List, Dict, Iterator

def cli_wrapper(**data: Dict):
    """Handler for the uniform distribution. Checks and cleans given options,
    and performs optional reporting.
    """
    _number = data["number"] if data["number"] is not None else 10
    _init_mu = data["mu"] if data["mu"] is not None else 0.0
    _sigma = data["sigma"] if data["sigma"] is not None else 1.0
    _init_velocity = data["delta"] if data["delta"] is not None else 0.0
    _acceleration = lambda x: x #constant acceleration

    _distribution = distribution(
        _init_mu,
        _sigma,
        _init_velocity,
        _acceleration,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(_init_mu, _sigma, _init_velocity, _acceleration)
        )
    if _number > 0:
        for number in itertools.islice(_distribution, _number):
            sys.stdout.write("{0:.4f}\n".format(number))

def distribution(
    init_mu: float,
    sigma: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
) -> Iterator[float]:
    mu = init_mu
    velocity = init_velocity
    while True:
        yield random.normalvariate(mu, sigma)
        mu += velocity
        velocity = acceleration(velocity)

# use this in a report function later: μ±
def report_header(
    init_mu: float,
    sigma: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
) -> str:
    _msg = (
        "Normal distribution",
        "  μ={0:.4f}, σ={1:.4f}".format(init_mu, sigma),
        "  dμ/dt={0:.4f}".format(init_velocity),
        "Obs.:",
        "========",
    )
    return "\n".join(_msg) + "\n"

