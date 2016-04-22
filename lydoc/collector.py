"""The collector module provides utilities to collect documentation elements
from Lilypond files and directories."""

from lydoc.lilyparser import LilyParser, LilySemantics
import re


# These two regular expressions are used by the strip_leading_comment function
# below.
_whitespace_only_re = re.compile('^[ \t%]+$', re.MULTILINE)
_leading_whitespace_re = re.compile('(^[ \t%]*)(?:[^ \t\n])', re.MULTILINE)


def strip_leading_comment(text):
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


class DocumentationSemantics(LydocSemantics):
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

    def embedded_scheme_pre(self, ast):
        """This semantic action changes the comment character before starting
        to parse scheme code.
        """
        self.old_eol_comments_re = ast.parseinfo.buffer.eol_comments_re
        ast.parseinfo.buffer.eol_comments_re = ";.*$"
        return ast

    def embedded_scheme_post(self, ast):
        """Undo the changes done by the function embedded_scheme_pre"""
        ast.parseinfo.buffer.eol_comments_re = self.old_eol_comments_re
        return ast

    def name_definition(self, ast):
        LOGGER.debug('Found name definition %s', ast.name)
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

    def scheme_parse_error(self, ast):
        pinfo = ast.parseinfo
        buffer = pinfo.buffer
        file = buffer.filename
        line = buffer.line_info(pinfo.pos).line
        LOGGER.error('Error while parsing scheme. (%s:%s)', file, line)
        raise FailedSemantics(
            'Error parsing embedded scheme. Unbalanced parentheses?')
