#!/usr/bin/env python3.7

# custom lib
from mylib.env import ENV, read_stdin
from mylib.cli import ARGS
from mylib.fs import File, exists

# typing
from typing import *


def read_args_or_stdin(*,
                       arg_number: int = 1,
                       opts: Tuple[str, ...] = ('f', 'files'),
                       opt_number: int = 1                    ) -> List[str]:
    """
    Input handler for well-behaved scripts.

    Checks for '-f' or '--file' command line options and N file names following
    them. Else check for the N first positional argument. Else assume STDIN. If
    '-' is found at any step, STDIN is used in place.

    Options:
      arg_number : Max num. of files from positional arguments  [Default: 1]
      opts       : File option flags [Default: 'f', 'file']
      opt_number : Max num. of files from file options [Default: 1]
    """
    # process cli
    fnames = ARGS.getany(opts, [], number=opt_number)
    positional = ARGS.positional()
    if not fnames and positional:
        fnames = positional[:arg_number]

    # build buffer
    if fnames:
        buffer = list()
        for fname in fnames:
            if fname == '-':
                buffer += read_stdin() # env.read_stdin
            elif exists(fname): # fs.exists
                buffer += File(fname).lines()
            else:
                pass # TODO: option for raising here
    else:
        buffer = read_stdin() # env.read_stdin

    return buffer

if __name__ == '__main__':
    lines = read_args_or_stdin()
    print('\n'.join(lines))

