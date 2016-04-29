"""The collector module provides utilities to collect documentation elements
from Lilypond files and directories."""

# For Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals


from lydoc.lilyparser import LilyParser, LilySemantics
from . import console
import re
import io
import os
from grako.exceptions import FailedParse, FailedSemantics
import logging


# These two regular expressions are used by the strip_leading_comment function
# below.
_whitespace_only_re = re.compile('^[ \t%]+$', re.MULTILINE)
_leading_whitespace_re = re.compile('(^[ \t%]*)(?:[^ \t\n])', re.MULTILINE)


def strip_leading_comments(text):
    """Strips the leading whitespaces and % from the given text.

    Adapted from textwrap.dedent
    """
    # Look for the longest leading string of spaces and tabs common to
    # all lines.
    margin = None
    text = _whitespace_only_re.sub('', text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent

        # Current line more deeply indented than previous winner:
        # no change (previous winner is still on top).
        elif indent.startswith(margin):
            pass

        # Current line consistent with and no deeper than previous winner:
        # it's the new winner.
        elif margin.startswith(indent):
            margin = indent

        # Current line and previous winner have no common whitespace:
        # there is no margin.
        else:
            margin = ""
            break

    # sanity check (testing/debugging only)
    if 0 and margin:
        for line in text.split("\n"):
            assert not line or line.startswith(margin), \
                "line = %r, margin = %r" % (line, margin)

    if margin:
        text = re.sub(r'(?m)^' + margin, '', text)
    return text


class DocumentationSemantics(LilySemantics):
    """Semantic actions to be performed during Grako parsing.

    See:
    https://pypi.python.org/pypi/grako#semantic-actions
    """

    def __init__(self, collected_elements):
        self.collected_elements = collected_elements

    def add_position_info(self, ast):
        pinfo = ast.parseinfo
        buffer = pinfo.buffer
        ast['file'] = buffer.filename
        ast['line'] = buffer.line_info(pinfo.pos).line

    def function_definition(self, ast):
        logging.debug("Found function definition %s", ast.name)
        self.add_position_info(ast)
        # Convert the AST to a simple dict, so that the grako buffer
        # associated with the parseinfo can be released when it is no
        # longer needed. Otherwise, the buffer is kept in memory
        # until the reference to this AST is kept in memory. When
        # dealing with many files this can lead to an excessive
        # memory usage.
        ast = dict(ast)
        ast['type'] = 'function'
        # Strip the comment character from the beginning of the line
        docs = ast['documentation']
        if docs is not None:
            stripped = strip_leading_comments(docs)
            ast['documentation'] = stripped
        self.collected_elements.append(ast)
        return ast

    def name_definition(self, ast):
        logging.debug('Found name definition %s', ast.name)
        self.add_position_info(ast)
        # Convert the AST to a simple dict, so that the grako buffer
        # associated with the parseinfo can be released when it is no
        # longer needed. Otherwise, the buffer is kept in memory
        # until the reference to this AST is kept in memory. When
        # dealing with many files this can lead to an excessive
        # memory usage.
        ast = dict(ast)
        ast['type'] = 'name'
        # Strip the comment character from the beginning of the line
        docs = ast['documentation']
        if docs is not None:
            stripped = strip_leading_comments(docs)
            ast['documentation'] = stripped
        self.collected_elements.append(ast)
        return ast

    def embedded_scheme_error(self, ast):
        pinfo = ast.parseinfo
        buf = pinfo.buffer
        fname = buf.filename
        line = buf.line_info(pinfo.pos).line
        raise FailedSemantics(
            "Error parsing embedded scheme (unbalanced parentheses?)")


def parse(target, trace=False, **kwargs):
    """Parse the given target. If it is a file-like object, then parse its
    contents. If given a string, perform one of the following actions

     - If the string is a valid file path, then open and parse it
     - If the string is a valid directory path, then recursively look for
       files ending in .ly or .ily
     - Otherwise parse the string directly.

    """

    # Beware! This function, that actually is the core of all the
    # business, is written to minimize the responsibilities of each
    # chunk of code, keeping things simple. Performance may degrade
    # because of this, but without actual measurements the simplest
    # choice is the best one.

    if hasattr(target, 'read'):
        # It's a file-like object
        file_content = target.read()
        return parse(file_content, trace, **kwargs)

    if os.path.isfile(target):
        if target.endswith(".ily") or target.endswith(".ly"):
            console.display("Parsing", target)
            with io.open(target, "r", encoding="utf-8") as fp:
                return parse(fp, trace, filename=target, **kwargs)
        else:
            return []

    if os.path.isdir(target):
        docs = []
        logging.info("Parsing directory {}", target)
        for root, _, files in os.walk(target):
            for f in files:
                fname = os.path.join(root, f)
                file_docs = parse(fname, trace, **kwargs)
                docs.extend(file_docs)
        return docs

    # We were given a text, so parse it directly
    metrics = kwargs.get("metrics", None)
    if metrics is not None:
        metrics.record_file(target)

    docs = []
    parser = LilyParser(parseinfo=True)
    try:
        parser.parse(target,
                     'lilypond',
                     semantics=DocumentationSemantics(docs),
                     filename=kwargs.get("filename", None),
                     trace=trace)
    except FailedParse as err:
        logging.warn(err)
        if metrics is not None:
            metrics.record_error(err)
    except RuntimeError as err:
        logging.warn(err)
        if metrics is not None:
            metrics.record_error(err)

    return docs
