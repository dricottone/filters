#!/usr/bin/env python3

"""rng notrandom [OPTIONS]
Generate non-random data.

Options:
  -d, --delta    velocity of state per time unit [Default: 0]
  -i, --initial  initial state [Default: 0]
  -n, --number   number of data points to generate [Default: 10]
"""

import sys
import itertools
from typing import Callable, List, Dict, Iterator

def cli_wrapper(**data: Dict):
    """Handler for the uniform distribution. Checks and cleans given options,
    and performs optional reporting.
    """
    _number = data["number"] if data["number"] is not None else 10
    _init_state = data["initial"] if data["initial"] is not None else 0.0
    _init_velocity = data["delta"] if data["delta"] is not None else 0.0
    _acceleration = lambda x: x #constant acceleration

    _distribution = distribution(
        _init_state,
        _init_velocity,
        _acceleration,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(_init_state, _init_velocity, _acceleration)
        )
    if _number > 0:
        for number in itertools.islice(_distribution, _number):
            sys.stdout.write("{0:.4f}\n".format(number))

def distribution(
    init_state: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
) -> Iterator[float]:
    """Generate non-random data.

    Arguments:
      init_state     initial value
      init_velocity  initial velocity of state per time unit
      acceleration   function of v1 <- v0
    """
    state = init_state
    velocity = init_velocity

    while True:
        yield state
        state += velocity
        velocity = acceleration(velocity)

def report_header(
    init_state: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
):
    """Draw a report header summarizing the distribution."""
    _msg = (
        "Not random data",
        "  Initial value of {0:.4f}, changing {1:.4f} per time unit".format(
            init_state, init_velocity,
        ),
        "Data:",
        "========",
    )
    return "\n".join(_msg) + "\n"

