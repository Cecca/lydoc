from nose.tools import *
from lydoc.lilyparser import LilyParser
from lydoc.collector import DocumentationSemantics
import grako


def parse(text, startrule, trace=False):
    docs = []
    parser = LilyParser(parseinfo=True)
    return parser.parse(text, startrule,
                        semantics=DocumentationSemantics(docs),
                        trace=trace)


def test_scheme_string():
    txt = '"This is a scheme string with ( unbalanced parentheses"'
    ast = parse(txt, 'scheme')
    assert_equals('"' + ast + '"', txt)


def test_scheme_list():
    txt="""(1 2 3 (4 5 6) 2)"""
    ast = parse(txt, 'scheme')
    assert_equals(
        ast, {'list': ['1', '2', '3', {'list': ['4', '5', '6']}, '2']})


@raises(grako.exceptions.FailedParse)
def test_scheme_unbalanced_list():
    txt="""(1 2 3 (4 5 6 2)"""
    ast = parse(txt, 'scheme')


def test_scheme_comment():
    txt="""
    ; This is a comment (:
    ;; With two leading semicolons
    (this is normal scheme)
    """
    ast = parse(txt, "scheme")
    assert_equals(
        ast, [["; This is a comment (:",
               ";; With two leading semicolons"],
              {'list': ['this', 'is', 'normal', 'scheme']}])


def test_embedded_scheme():
    txt = """
    #(This is some embedded scheme
    ; With inline comments (unbalanced parens
    "And strings :)")
    """
    ast = parse(txt, "embedded_scheme")
    assert_equals(
        ast,
        ['#',
         {'list': ['This', 'is', 'some', 'embedded', 'scheme',
                       [['; With inline comments (unbalanced parens'],
                        'And strings :)']]}])


@raises(grako.exceptions.FailedParse)
def test_embedded_scheme_error():
    txt = """
    #((This is some embedded scheme
    ; With inline comments (unbalanced parens
    "And strings :)")
    """
    ast = parse(txt, "embedded_scheme")
    assert_equals(
        ast, '#')
