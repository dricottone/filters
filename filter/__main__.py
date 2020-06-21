#!/usr/bin/env python3

import sys

from . import cli
from . import internals

def main():
    _config, _positionals = cli.main(sys.argv[1:])

    if "version" in _config.keys():
        internals._print_version()
        sys.exit(0)
    elif "list-methodologies" in _config.keys():
        internals._print_methodologies("ab", "convolve")
        sys.exit(0)
    elif "methodology" in _config.keys():
        _method = config.get("methodology", "")
    elif len(_positionals) > 0:
        _method = _positionals.pop(0)
    elif "help" in _config.keys():
        internals._print_help()
        sys.exit(0)
    else:
        internals._print_usage()
        sys.exit(1)

    _init_estimate = 0
    _init_deviation = 1
    if "initial" in _config.keys():
        _initial = internals._try_get_list_float(_config, "initial")
        if len(_initial) > 1:
            _init_estimate = _initial[0]
            _init_deviation = _initial[1]
        elif len(_initial) == 1:
            _init_estimate = _initial[0]

    _data = {
        "alpha": internals._try_get_float(_config, "alpha"),
        "beta": internals._try_get_float(_config, "beta"),
        "delta": internals._try_get_float(_config, "delta"),
        "initial_estimate": _init_estimate,
        "initial_std_deviation": _init_deviation,
        "kernel": internals._try_get_list_float(_config, "kernel"),
        "method": _method,
        "report": "report" in _config.keys(),
        "variance": internals._try_get_float(_config, "variance"),
    }

    if _method == "ab":
        from . import ab as implementation
    elif _method == "kalman":
        from . import kalman as implementation
    elif _method == "convolve":
        from . import convolve as implementation
    elif len(_method) > 0:
        internals._print_invalid_methodology(_method)
        internals._print_usage()
        sys.exit(1)

    if "help" in _config.keys():
        sys.stdout.write(implementation.__doc__)
        sys.exit(0)

    _files = _config.get("file", [])
    _files.extend(_positionals)
    _data["data_raw"] = internals._get_raw_data(_files)
    implementation.cli_wrapper(**_data)

    sys.exit(0)

if __name__ == "__main__":
    main()

