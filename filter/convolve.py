#!/usr/bin/env python3

"""filter convolve [OPTIONS] DATA
Convolution filter - Filter out noise of measurements to estimate data.

Options:
  -k KERNEL,         filter data through KERNEL, where KERNEL is one or more
    --kernel KERNEL    numeric factors [Default: 1.0]
"""

__all__ = ['cli_wrapper', 'filter', 'report']

import sys
from typing import List, Dict, Iterator

def cli_wrapper(
        **data: Dict,
) -> None:
    """Handler for the convolution filter. Checks and cleans given options,
    and performs optional reporting.
    """
    _kernel = _normalize(
        data["kernel"] if data["kernel"] is not None else [1.0]
    )
    _raw = data["data_raw"]

    _filter = filter(
        _raw,
        _kernel,
    )

    if data["report"]:
        sys.stdout.write(report_header(_kernel))
        for measured, estimated in zip(_raw, _filter):
            sys.stdout.write("{0:8.4f}  {1:8.4f}\n".format(measured, estimated))
    else:
        for estimated in _filter:
            sys.stdout.write("{0:.4f}\n".format(estimated))

def filter(
    data: List[float],
    kernel: List[float]
) -> Iterator[float]:
    """Iterate over data, passing it through the kernel.

    Arguments:
      data    measurements
      kernel  measurement adjustments
    """
    length = len(data)
    #NOTE: for evenly-sized kernels, extra goes to top and left
    offset = len(kernel) // 2

    for index in range(length):
        _sum = 0.0
        for kernel_index, kernel_point in enumerate(kernel, start=-offset):
            target = (index + kernel_index) % length
            _sum += data[target] * kernel_point
        yield _sum

def report_header(
    kernel: List[float],
) -> str:
    """Draw a report header summarizing the filter.

    Appears as:
    ```
    Convolution filter
      kernel=[<value1> ... <valueK>]
    Raw:      Est.:
    ========  ========
    ```

    The estimates then should be printed alongside the raw measurements.
    """
    _msg = (
        "Convolution filter",
        "  kernel={0}".format(kernel),
        "Raw:      Est.:",
        "========  ========",
    )
    return "\n".join(_msg) + "\n"

def _normalize(kernel: List[float]) -> List[float]:
    _sum = sum(kernel)
    if _sum == 1:
        return kernel
    else:
        weight = 1.0/_sum
        return [factor * weight for factor in kernel]

