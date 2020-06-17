#!/usr/bin/env python3

import sys

from . import cli
from . import internals

def main():
    _config, _positionals = cli.main(sys.argv[1:])

    _method = _config.get("method", "")
    _data = {
        "alpha": internals._try_get_float(_config, "alpha"),
        "beta": internals._try_get_float(_config, "beta"),
        "delta": internals._try_get_float(_config, "delta"),
        "initial": internals._try_get_float(_config, "initial"),
        "method": _method,
        "report": "report" in _config.keys(),
        "time": internals._try_get_float(_config, "time"),
    }

    if "version" in _config.keys():
        internals._print_version()
        sys.exit(0)

    if _method == "ab":
        from . import ab as implementation
    elif len(_method) > 0:
        # if some methodology given but not in above list
        internals._print_invalid_methodology(_method)
        internals._print_usage()
        sys.exit(1)

    if "help" in _config.keys() and "method" not in _config.keys():
        # requesting help
        internals._print_help()
        sys.exit(0)
    elif "help" in _config.keys():
        # requesting help with a methodology
        sys.stdout.write(implementation.__doc__)
        sys.exit(0)
    elif "method" not in _config.keys():
        # not requesting help, but still no methodology
        internals._print_usage()
        sys.exit(1)

    _files = _config.get("file", [])
    _files.extend(_positionals)
    _data["data_raw"] = internals._get_raw_data(_files)
    implementation.cli_wrapper(**_data)

    sys.exit(0)

if __name__ == "__main__":
    main()

