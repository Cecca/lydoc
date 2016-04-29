"""Output to the console. This function is for normal output, therefore we
don't use the logging module. We don't use a plain print either, because we
want the output to standard error: standard output is reserved for data, e.g.
the json representation of the documentation"""

# For Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

import sys


def display(*args):
    print(*args, file=sys.stderr)

