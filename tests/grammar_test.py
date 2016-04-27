from nose.tools import *
from lydoc.lilyparser import LilyParser
from lydoc.collector import DocumentationSemantics
from pprint import pprint
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


def test_name_definition():
    txt = """
    %{!
    % Doc comment
    %}
    someFunc = #(the scheme code)
    """
    ast = parse(txt, 'lilypond')
    assert_equals(
        ast,
        [{'documentation': '\nDoc comment\n',
          'file': '',
          'line': 1,
          'name': 'someFunc',
          'type': 'name'},
         ['#', {'list': ['the', 'scheme', 'code']}]])



def test_name_definition_simple_comment():
    txt = """
    %{
    % Simple comment
    %}
    someFunc = #(the scheme code)

    %% Another comment
    """
    ast = parse(txt, 'lilypond')
    pprint(ast)
    assert_equals(
        ast,
        ['%{\n    % Simple comment\n    %}',
         {'documentation': None,
          'file': '',
          'line': 4,
          'name': 'someFunc',
          'type': 'name'},
         ['#', {'list': ['the', 'scheme', 'code']}],
        ["%% Another comment"]])


def test_function_definition():
    txt="""
    %{!
    % This is a function definition
    %}
    func =
    #(define-music-function
      (parser location param-a param-b) (string? music?)
      (do things))
    """
    ast = parse(txt, 'function_definition')
    assert_equal(
        ast,
        {'documentation': '\nThis is a function definition\n',
         'file': '',
         'functionType': 'music',
         'line': 0,
         'name': 'func',
         'parameters': ['param-a', 'param-b'],
         'parameterTypes': ['string?', 'music?'],
         'type': 'function'})


def test_function_definition_2_19():
    txt="""
    %{!
    % This is a function definition
    %}
    func =
    #(define-music-function
      (param-a param-b) (string? music?)
      (do things))
    """
    ast = parse(txt, 'function_definition')
    assert_equal(
        ast,
        {'documentation': '\nThis is a function definition\n',
         'file': '',
         'functionType': 'music',
         'line': 0,
         'name': 'func',
         'parameters': ['param-a', 'param-b'],
         'parameterTypes': ['string?', 'music?'],
         'type': 'function'})
