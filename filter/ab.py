#!/usr/bin/env python3

"""filter ab [OPTIONS] DATA
Alpha-beta filter - Filter out noise of measurements to estimate data.

Options:
  -a N, --alpha N  correction to estimated state [Default: 0.05]
  -b N, --beta N   correction to estimated velocity of state [Default: 0.005]
  -d N, --delta N  initial velocity of state per time unit [Default: 0]
  -i M N,          initial state; M is the estimate and N is the std. deviation
    --initial M N    [Note: std. deviation unused] [Default: 0 0]

Currently assumed that acceleration is constant and that the time unit is 1.
"""

__all__ = ['cli_wrapper', 'filter', 'report']

import sys
from typing import Callable, List, Dict, Iterator

def cli_wrapper(**data: Dict):
    """Handler for the alpha-beta filter. Checks and cleans given options,
    and performs optional reporting.
    """
    _raw = data["data_raw"]
    _alpha = data["alpha"] if data["alpha"] is not None else 0.05
    _beta = data["beta"] if data["beta"] is not None else 0.005
    _init_state = data["initial_estimate"]
    _init_velocity = data["delta"] if data["delta"] is not None else 0

    _time = 1.0 #constant time unit
    _acceleration = lambda x: x #constant acceleration

    _filter = filter(
        _raw,
        _alpha,
        _beta,
        _init_state,
        _init_velocity,
        _acceleration,
        _time,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(
                _alpha,
                _beta,
                _init_state,
                _init_velocity,
                _acceleration,
                _time,
            )
        )
        for measured, estimated in zip(_raw, _filter):
            sys.stdout.write("{0:8.4f}  {1:8.4f}\n".format(measured, estimated))
    else:
        for estimated in _filter:
            sys.stdout.write("{0:.4f}\n".format(estimated))

def filter(
    data: List[float],
    alpha: float,
    beta: float,
    init_state: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
    time: float,
) -> Iterator[float]:
    """Iterate over data, passing it through an alpha-beta filter.

    Arguments:
      data           measurement from each time interval
      alpha          correction to estimated state
      beta           correction to estimated velocity
      acceleration   function of v1 <- v0
      init_state     initial estimate of state
      init_velocity  initial estimate of velocity
      time           time unit
    """
    last_estimated = init_state
    last_velocity = init_velocity
    for data_point in data:
        #estimate given last values
        estimated = last_estimated + (time * last_velocity)
        velocity = acceleration(last_velocity)

        #correct for residual
        residual = (data_point - estimated)
        estimated += (alpha * residual)
        velocity += ( (beta * residual) / time )

        last_estimated = estimated
        last_velocity = velocity

        yield estimated

def report_header(
    alpha: float,
    beta: float,
    init_state: float,
    init_velocity: float,
    acceleration: Callable[[float], float],
    time: float,
) -> str:
    """Draw a report header summarizing the filter.

    Appears as:
    ```
    Alpha-beta filter
      α=<alpha>,β=<beta>
      Initial estimate: <init_state> changing <init_velocity> per time unit
    Raw:      Est.:
    ========  ========
    ```
    The estimates then should be printed alongside the raw measurements.
    """
    _msg = (
        "Alpha-beta filter",
        "  α={0:.4f}, β={1:.4f}".format(alpha, beta),
        "  Initial estimate: {0:.4f} changing {1:.4f} per time unit".format(
            init_state, init_velocity,
        ),
        "Raw:      Est.:",
        "========  ========",
    )
    return "\n".join(_msg) + "\n"

