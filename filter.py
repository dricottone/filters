#!/usr/bin/env python3

# std library
import random

# custom library
from mylib.cli import ARGS, read_args_or_stdin, set_verbosity

# typing
from typing import *

def ab(data: List[float],
       *,
       alpha: float,
       beta: float,
       acceleration: Callable[[float], float] = lambda x: x,
       init_state: float = 0,
       init_velocity: float = 0,
       time: float = 1
      ) -> List[float]:
    """
    Alpha-beta filter - Filter out noise of measurements to estimate data.
    Takes as given:
      initial state
      initial velocity of state
      alpha and beta correction parameters

    Arguments:
      data          : measurements of state
      alpha         : correction to estimated state
      beta          : correction to estimated velocity of state
    Options:
      acceleration  : function f such that v1 <- f(v0) [Default: v1 <- v0]
      init_state    : initial state estimate [Default: 0]
      init_velocity : initial velocity of state [Default: 0]
      time          : the time unit [Default: 1]
    """
    estimates = list()
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

        estimates.append(x_est)

    return estimates

# ^ filters
###############################################################################
# v internal functions

def noise(data: List[float]) -> List[float]:
    """
    Introduce random noise (r in [-1,1]) to a set of data points.
    """
    def _noise_iter(data: List[float]) -> Iterator[float]:
        for d in data:
            yield d + random.uniform(-1,1)
    return list(_noise_iter(data))

# ^ internal functions
###############################################################################
# v cli functions

def print_help():
    print("Usage: filter -m=METHOD DATA")

def get_data():
    data = list()
    for d in read_args_or_stdin(arg_number=-1, opt_number=-1,
                                opts=('f', 'files')):
        if not len(d):
            continue
        else:
            data.append( float(d) )
    return data

def report_est(data, estimations, alpha, beta, initial_state, initial_velocity):
    """
    Prints a report on the estimations to STDOUT.
    """
    print("Testing on N={}".format(len(data)))
    print("Using alpha={:.4f}, beta={:.4f}".format(alpha,beta))
    print("Initial estimate of {:.4f}, accelerating {:.4f} per time unit".format(initial_state,initial_velocity))
    print("  Actual:   Est.:  \n  ========  ========")
    for d,e in zip(data,estimations):
        print("  {:8.4f}  {:8.4f}".format(d,e))

def print_est(estimations):
    """
    Prints the estimations to STDOUT with 4 decimal places of accuracy.
    """
    for e in estimations:
        print("{:.4f}".format(e))

# ^ cli functions
###############################################################################

if __name__ == '__main__':
    import sys

    set_verbosity()
    if len(sys.argv) < 2 or ARGS.any('h', 'help'):
        print_help()
        sys.exit(0)

    method = ARGS.getany(('m', 'method'), number=1)
    try:
        _method = locals()[method]
    except: # if no method specified, or if bad method specified
        print(f'Invalid method {method}')
        print_help()
        sys.exit(1)

    data = get_data()
    if not data:
        print_help()
        sys.exit(1)

    alpha = ARGS.getany(('a', 'alpha'), .05, factory=float, number=1)
    beta = ARGS.getany(('b', 'beta'), .005, factory=float, number=1)
    initial = ARGS.getany(('i', 'initial'), 0, factory=float, number=1)
    delta = ARGS.getany(('d', 'delta'), 0, factory=float, number=1)
    report = ARGS.any('r', 'report')

    est = _method(data,
                  alpha=alpha,
                  beta=beta,
                  init_state=initial,
                  init_velocity=delta
                 )
    if report:
        report_est(data, est, alpha, beta, initial, delta)
    else:
        print_est(est)
    sys.exit(0)

