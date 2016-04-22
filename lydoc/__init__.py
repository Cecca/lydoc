"""Lydoc is a simple API documentation generator for lilypond."""

from . import collector, console, renderer
import argparse
import sys
import logging
import pprint
import colorama
from jinja2.exceptions import TemplateNotFound


def _cli_argument_parser():
    argp = argparse.ArgumentParser(
        description='Produce Lilypond documentation')

    argp.add_argument(
        'path', metavar='PATH',
        help='The file or directory to parse')

    argp.add_argument(
        '--output', '-o', metavar='FILE',
        help='The output file. If not given, prints to standard output')

    argp.add_argument(
        '--trace-parser', action='store_true', dest='trace_parser',
        help='Print debug information from the parser')

    argp.add_argument(
        '-d', '--debug',
        help="Detailed debugging information",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING)
    argp.add_argument(
        '-v', '--verbose',
        help="Verbose output",
        action="store_const", dest="loglevel", const=logging.INFO)

    return argp


def main():
    """The main entry point of the program"""

    colorama.init()

    # Parse command line arguments
    argp = _cli_argument_parser()
    args = argp.parse_args()

    # setup logging
    logging.basicConfig(level=args.loglevel)

    console.display(console.action("Collecting"), "documentation from files")
    docs = collector.parse(args.path, args.trace_parser)

    console.display(console.action("Rendering"), "documentation")
    try:
        out = renderer.render_template(docs, "markdown.")
    except TemplateNotFound as err:
        logging.error(
            "Template `{}` not found. Available templates are: {}".format(
                err.name, renderer.JINJA_ENV.list_templates()))
        sys.exit(1)
    print(out)
