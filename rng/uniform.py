#!/usr/bin/env python3

"""rng uniform [OPTIONS]
Uniform distribution - Generate random data from a uniform distribution.

Options:
  -d, --delta   velocity of average per time unit [Default: 0]
  -m, --mu      average of distribution [Default: 0]
  -n, --number  number of random data points to generate [Default: 10]
  -o, --offset  distance from average to bounds of distribution [Default: 1]

Currently assumed that offset is constant over time.
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
    _offset = data["offset"] if data["offset"] is not None else 1.0
    _init_velocity = data["delta"] if data["delta"] is not None else 0.0
    _acceleration = lambda x: x #constant acceleration

    _distribution = distribution(
        _init_mu,
        _offset,
        _init_velocity,
        _acceleration,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(_init_mu, _offset, _init_velocity, _acceleration)
        )
    if _number > 0:
        for number in itertools.islice(_distribution, _number):
            sys.stdout.write("{0:.4f}\n".format(number))

def distribution(
    init_mu: float,
    offset: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
) -> Iterator[float]:
    """Generate random data.

    Arguments:
      init_mu        initial average of distribution
      offset         distance from average to distribution bounds
      init_velocity  initial velocity of average per time unit
      acceleration   function of v1 <- v0
    """
    mu = init_mu
    velocity = init_velocity
    while True:
        yield mu + random.uniform(-offset,offset)
        mu += velocity
        velocity = acceleration(velocity)

def report_header(
    init_mu: float,
    offset: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
):
    """Draw a report header summarizing the distribution."""
    _msg = (
        "Uniform distribution",
        "  μ={0:.4f}, [{1:.4f},{2:.4f}]".format(
            init_mu, init_mu-offset, init_mu+offset,
        ),
        "  dμ/dt={0:.4f}".format(init_velocity),
        "Obs.:",
        "========",
    )
    return "\n".join(_msg) + "\n"

