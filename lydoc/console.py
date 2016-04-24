"""Output to the console. This function is for normal output, therefore we
don't use the logging module. We don't use a plain print either, because we
want the output to standard error: standard output is reserved for data, e.g.
the json representation of the documentation"""

import sys


def display(*args):
    print(*args, file=sys.stderr)

