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

def _try_get_list_float(
    mapping: Dict,
    key: str,
    *,
    default: Optional[List[float]] = None,
) -> Optional[List[float]]:
    if key in mapping:
        _list = list()
        for value in mapping[key]:
            try:
                _list.append(float(value))
            except:
                _print_invalid_data(value)
        return _list
    else:
        return default

def _read_stdin() -> Iterator[float]:
    try:
        for line in sys.stdin.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            try:
                yield float(line.strip())
            except:
                _print_invalid_data(line)
    except KeyboardInterrupt:
        sys.stdout.write("\n")

def _read_file(filename: str) -> Iterator[float]:
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                try:
                    yield float(line)
                except:
                    _print_invalid_data(line)
    except OSError:
        _print_invalid_file(filename)

def _get_raw_data(filenames: List[str]) -> List[float]:
    raw_data: List[float] = list()

    if len(filenames) == 0:
        raw_data.extend(list(_read_stdin()))
    else:
        for filename in filenames:
            if filename == '-':
                raw_data.extend(list(_read_stdin()))
            else:
                raw_data.extend(list(_read_file(filename)))

    return raw_data

def _print_help() -> None:
    _msg = "Usage: filter METHOD [OPTIONS] DATA\n"
    sys.stdout.write(_msg)

def _print_version() -> None:
    _msg = "filter {0}\n".format(".".join(str(v) for v in VERSION))
    sys.stdout.write(_msg)

def _print_methodologies(*method: str) -> None:
    _msg = "Valid methodologies: {0}\n".format(", ".join(method))
    sys.stdout.write(_msg)

def _print_usage() -> None:
    _msg = (
        "Usage: filter METHOD [OPTIONS] DATA",
        "Try `filter --list-methodologies` and `filter METHOD --help`",
    )
    sys.stderr.write("\n".join(_msg) + "\n")

def _print_invalid_methodology(method: str) -> None:
    _msg = (
        "{0}: Invalid methodology '{1}'\n".format(sys.argv[0], method),
        "Try `filter --list-methodologies`",
    )
    sys.stderr.write("\n".join(_msg) + "\n")

def _print_invalid_file(filename: str) -> None:
    _msg = "{0}: Invalid file '{1}'\n".format(sys.argv[0], filename)
    sys.stderr.write(_msg)

def _print_invalid_data(line: str) -> None:
    _msg = "{0}: Cannot convert '{1}' into numeric value\n".format(
        sys.argv[0], line,
    )
    sys.stderr.write(_msg)

