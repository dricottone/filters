#!/usr/bin/env python3

"""filter kalman [OPTIONS] DATA
Kalman filter - Filter out normally-distributed noise of measurements to
estimate data.

Options:
  -d, --delta     initial velocity of state per time unit [Default: 0]
  -i, --inital    initial estimate of state [Default: 0]
  -s, --sigma     initial std. deviation of state distribution [Default: 1]
  -v, --variance  variance of data measurements [Default: 1]

Currently assumed that acceleration is 0, velocity is non-variate, and the time
unit is 1.
"""

__all__ = ['cli_wrapper', 'filter', 'report']

import sys
from typing import Callable, List, Dict, Iterator, Tuple

def cli_wrapper(**data: Dict):
    """Handler for the Kalman filter. Checks and cleans given options,
    and performs optional reporting.
    """
    _raw = data["data_raw"]
    _variance = data["variance"] if data["variance"] is not None else 1
    _init_state_mu = data["initial_estimate"]
    _init_state_sigma = data["initial_std_deviation"]
    _init_velocity_mu = data["delta"] if data["delta"] is not None else 0

    _init_velocity_sigma = 0 #non-variate velocity
    _time = 1.0 #constant time unit
    _acceleration = lambda x: x #constant acceleration


    _filter = filter(
        _raw,
        _variance,
        _init_state_mu,
        _init_state_sigma,
        _init_velocity_mu,
        _init_velocity_sigma,
        _acceleration,
        _time,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(
                _variance,
                _init_state_mu,
                _init_state_sigma,
                _init_velocity_mu,
                _init_velocity_sigma,
                _acceleration,
                _time,
            ),
        )
        for measured, filtered in zip(_raw, _filter):
            estimated, variance = filtered
            sys.stdout.write(
                "{0:8.4f}  {1:8.4f}  {2:8.4f}\n".format(
                    measured, estimated, variance,
                ),
            )
    else:
        for estimated, _ in _filter:
            sys.stdout.write("{0:.4f}\n".format(estimated))

def filter(
    data: List[float],
    variance: float,
    init_state_mu: float,
    init_state_sigma: float,
    init_velocity_mu: float,
    init_velocity_sigma: float,
    acceleration: Callable[[Tuple[float, float]], Tuple[float,float]],
    time: float,
) -> Iterator[Tuple[float,float]]:
    """Iterate over data, passing it through an alpha-beta filter.

    Arguments:
      data                 measurement from each time interval
      variance             variance of measurements
      init_state_mu        initial estimate of state
      init_state_sigma     std. deviation of state distribution
      init_velocity_mu     initial estimate of velocity
      init_velocity_sigma  std. deviation of velocity distribution
      acceleration         function of v1 <- v0
      time                 time unit
    """
    # normal distributions as tuples: (E(x), Var(x), )
    estimated = (init_state_mu, init_state_sigma**2, )
    velocity = (init_velocity_mu, init_velocity_sigma**2, )

    for measurement in data:
        estimated = _add(estimated, _multiply(velocity, (time,0,)))
        velocity = acceleration(velocity)

        estimated = _multiply(estimated, (measurement, variance, ))

        yield estimated

def report_header(
    variance: float,
    init_state_mu: float,
    init_state_sigma: float,
    init_velocity_mu: float,
    init_velocity_sigma: float,
    acceleration: Callable[[float], float],
    time: float,
) -> str:
    """Draw a report header summarizing the filter.

    Appears as:

    ```
    Kalman filter
      Distribution of estimated initial state: N(<mu>,<sigma>)
      Distribution of expected change per time unit: N(<mu>,<sigma>)
      Variance of measurements: <variance>
    Raw:      Est.:     Var.:
    ========  ========  ========
    ```

    The estimates and variances then should be printed alongside the raw
    measurements.
    """
    _msg = (
        "Kalman filter",
        "  Distribution of estimated initial state: N({0},{1}²)".format(
            init_state_mu, init_state_sigma,
        ),
        "  Distribution of expected change per time unit: N({0},{1}²)".format(
            init_velocity_mu, init_velocity_sigma,
        ),
        "  Variance of measurements: {0}".format(variance),
        "Raw:      Est.:     Var.:",
        "========  ========  ========",
    )
    return "\n".join(_msg) + "\n"

def _add(
    x: Tuple[float, float],
    y: Tuple[float, float],
) -> Tuple[float, float]:
    """Add a normal distribution to another normal distribution or a constant.

    In the case of two normal distributions (X and Y), the resultant values
    are:
      E(X + Y) = E(X) + E(Y)
      Var(X + Y) = Var(X) + Var(Y)

    In the case of a normal distribution (X) and a constant (C), the resultant
    values are:
      E(X + C) = E(X) + C
      Var(X + C) = Var(X)
    """
    if y[1] == 0:
        z = (x[0]+y[0], x[1], )
    else:
        z = (x[0]+y[0], x[1]+y[1], )
    return z

def _multiply(
    x: Tuple[float, float],
    y: Tuple[float, float],
) -> Tuple[float, float]:
    """Multiply a normal distribution by another normal distribution or by a
    constant.

    Given two normal distributions (X and Y), the resultant values are:
      E(X * Y) = (Var(Y)E(X) + Var(X)E(Y)) / (Var(X) + Var(Y))
      Var(X * Y) = (Var(X)Var(Y)) / (Var(X) + Var(Y))

    Given a normal distribution (X) and a constant (C), the resultant values
    are:
      E(X * C) = E(X) * C
      Var(X * C) = Var(X) * (C^2)
    """
    #_print_normal_distribution(x, "X")
    #_print_normal_distribution(y, "Y")
    if y[1] == 0:
        z = ((x[0] * y[0]), (x[1] * y[0]**2), )
    else:
        _denom = x[1] + y[1]
        _mean = ((x[0] * y[1]) + (y[0] * x[1])) / _denom
        _var = (x[1] * y[1]) / _denom
        z = (_mean, _var, )
    #_print_normal_distribution(z, "Z")
    return z

def _print_normal_distribution(
    x: Tuple[float, float],
    name: str,
) -> None:
    sys.stdout.write("{0} = N({1},{2})\n".format(name, x[0], x[1]))

