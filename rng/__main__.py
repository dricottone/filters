#!/usr/main/env python3

import sys

from . import cli
from . import internals

def main():
    _config, _positionals = cli.main(sys.argv[1:])

    if "version" in _config.keys():
        internals._print_version()
        sys.exit(0)
    elif "list-distributions" in _config.keys():
        internals._print_distributions("normal", "uniform", "notrandom")
        sys.exit(0)
    elif "distribution" in _config.keys():
        _dist = config.get("distribution", "")
    elif len(_positionals) > 0:
        _dist = _positionals.pop(0)
    elif "help" in _config.keys():
        internals._print_help()
        sys.exit(0)
    else:
        internals._print_usage()
        sys.exit(1)

    _data = {
        "delta": internals._try_get_float(_config, "delta"),
        "distribution": _dist,
        "initial": internals._try_get_float(_config, "initial"),
        "mu": internals._try_get_float(_config, "mu"),
        "number": internals._try_get_int(_config, "number"),
        "offset": internals._try_get_float(_config, "offset"),
        "report": "report" in _config.keys(),
        "sigma": internals._try_get_float(_config, "sigma"),
    }

    if _dist == "uniform":
        from . import uniform as implementation
    elif _dist == "normal":
        from . import normal as implementation
    elif _dist == "notrandom":
        from . import notrandom as implementation
    elif len(_dist) > 0:
        internals._print_invalid_distribution(_dist)
        internals._print_usage()
        sys.exit(1)
    if "help" in _config.keys():
        sys.stdout.write(implementation.__doc__)
        sys.exit(0)

    implementation.cli_wrapper(**_data)

    sys.exit(0)

if __name__ == "__main__":
    main()

