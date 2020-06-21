#!/usr/bin/env python3

import sys
from typing import *

VERSION = (1,0,1,)

def _try_get_float(
    mapping: Dict,
    key: str,
    *,
    default: Optional[float] = None,
) -> Optional[float]:
    if key in mapping:
        return float(mapping[key])
    else:
        return default

def _try_get_int(
    mapping: Dict,
    key: str,
    *,
    default: Optional[float] = None,
) -> Optional[float]:
    if key in mapping:
        return int(mapping[key])
    else:
        return default

def _print_help() -> None:
    _msg = "Usage: rng DISTRIBUTION [OPTIONS]\n"
    sys.stdout.write(_msg)

def _print_version() -> None:
    _msg = "rng {0}\n".format(".".join(str(v) for v in VERSION))
    sys.stdout.write(_msg)

def _print_distributions(*dist: str) -> None:
    _msg = "Valid distributions: {0}\n".format(", ".join(dist))
    sys.stdout.write(_msg)

def _print_usage() -> None:
    _msg = (
        "Usage: rng DISTRIBUTION [OPTIONS]",
        "Try `rng --list-distributions` and `rng DISTRIBUTION --help`",
    )
    sys.stderr.write("\n".join(_msg) + "\n")

def _print_invalid_distribution(dist: str) -> None:
    _msg = (
        "{0}: Invalid distribution '{1}'".format(sys.argv[0], dist),
        "Try `rng --list-distributions`",
    )
    sys.stderr.write("\n".join(_msg) + "\n")

