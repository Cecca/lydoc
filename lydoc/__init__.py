"""Lydoc is a simple API documentation generator for lilypond."""

# For Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals


from . import collector, console, renderer, metrics
import argparse
import sys
import logging
import pprint
import io
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

    # Parse command line arguments
    argp = _cli_argument_parser()
    args = argp.parse_args()

    # setup logging
    logging.basicConfig(
        level=args.loglevel,
        format="%(levelname)s %(message)s")

    console.display("Collecting documentation from files")
    collector_metrics = metrics.Metrics()
    docs = collector.parse(args.path, args.trace_parser,
                           metrics=collector_metrics)
    collector_metrics.display()

    console.display("Rendering documentation")

    try:
        if args.output:
            template = renderer.template_from_filename(args.output)
        else:
            template = "json"
        out = renderer.render(docs, template)
    except ValueError as err:
        logging.error(err)
        sys.exit(1)
    except TemplateNotFound as err:
        logging.error(
            "Template `{}` not found. Available templates are: {}".format(
                err.name, renderer.list_templates()))
        sys.exit(1)

    if not args.output:
        print(out)
    else:
        console.display("Writing documentation to", args.output)
        with io.open(args.output, "w", encoding="utf-8") as fp:
            fp.write(out)

