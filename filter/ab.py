#!/usr/bin/env python3

"""filter -m=ab [OPTIONS] <DATA>
Alpha-beta filter - Filter out noise of measurements to estimate data.

Options:
  -a, --alpha  correction to estimated state [Default: 0.05]
  -b, --beta   correction to estimated velocity of state [Default: 0.005]
  -d, --delta  initial velocity [Default: 0]
  -i, --inital initial state [Default: 0]
  -t, --time   unit of time [Default: 1]

Currently, assumes the function of acceleration (i.e. `v1 <- f(v0)`) is
`v1 <- v0`.
"""

__all__ = ['cli_wrapper', 'filter', 'report']

import sys

from typing import Callable, List, Dict, Iterator


def cli_wrapper(**data: Dict):
    """Handler for the alpha-beta filter. Checks and cleans given options,
    and performs optional reporting.
    """
    _alpha = data["alpha"] if data["alpha"] is not None else 0.05
    _beta = data["beta"] if data["beta"] is not None else 0.005
    _init_state = data["initial"] if data["initial"] is not None else 0
    _init_velocity = data["delta"] if data["delta"] is not None else 0
    _time = data["time"] if data["time"] is not None else 1.0
    _raw = data["data_raw"]

    _acceleration = lambda x: x #constant acceleration

    _filter = filter(
        _raw,
        _alpha,
        _beta,
        _acceleration,
        _init_state,
        _init_velocity,
        _time,
    )

    if data["report"]:
        sys.stdout.write(
            report_header(_alpha, _beta, _init_state, _init_velocity)
        )
        for actual, estimated in zip(_raw, _filter):
            sys.stdout.write("{0:8.4f}  {1:8.4f}\n".format(actual, estimated))
    else:
        for estimated in _filter:
            sys.stdout.write("{0:.4f}\n".format(estimated))


def filter(
    data: List[float],
    alpha: float,
    beta: float,
    acceleration: Callable[[float], float],
    init_state: float,
    init_velocity: float,
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
    x_last = init_state
    v_last = init_velocity
    for index, data_point in enumerate(data):
        #estimate given last values
        x_est = x_last + (time * v_last)
        v_est = acceleration(v_last)

        #correct for residual
        x_res = (data_point - x_est)
        x_est += (alpha * x_res)
        v_est += ( (beta * x_res) / time )

        x_last = x_est
        v_last = v_est

        yield x_est


def report_header(
    alpha: float,
    beta: float,
    init_state: float,
    init_velocity: float,
) -> str:
    """Draw a report header summarizing the filter.

    Appears as:
    ```
    Alpha-beta filter
      α=<alpha>,β=<beta>
      Initial estimate <init_state> changing <init_velocity> per time unit
    Actual:   Est.:
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
        "Actual:   Est.:",
        "========  ========",
    )
    return "\n".join(_msg) + "\n"

