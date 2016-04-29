"""Functions to render the collected documentation to various formats"""


# For Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals


import json
import jinja2
import os
from itertools import groupby


JINJA_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader('lydoc', 'templates'))


def list_templates():
    return JINJA_ENV.list_templates()


def _build_templates_map():
    m = {
        # json is kind of a special value, it does not correspond to a jinja
        # template. See the function `render` to see how it's used
        "json": ["json"],
        "markdown.j2": ["md", "markdown", "mdown"],
        "restructuredtext.j2": ["rst"]
    }

    tmap = dict()
    for template, extensions in m.items():
        for ext in extensions:
            tmap[ext] = template
    return tmap


TEMPLATES_MAP = _build_templates_map()


def template_from_filename(filename):
    """Returns the appropriate template name based on the given file name."""
    ext = filename.split(os.path.extsep)[-1]
    if not ext in TEMPLATES_MAP:
        raise ValueError("No template for file extension {}".format(ext))
    return TEMPLATES_MAP[ext]


def render_json(docs):
    """Represent each doc in docs as a json object, one per line"""
    return "\n".join([json.dumps(doc) for doc in docs]) + "\n"


def render_template(docs, template):
    grouped_docs = {f: list(sorted(list(dl), key=lambda d: d['name']))
                    for f, dl in groupby(docs, lambda d: d['file'])}
    template = JINJA_ENV.get_template(template)
    rendered = template.render(documentation=grouped_docs,
                               trim_blocks=True,
                               lstrip_blocks=True)
    return rendered


def render(docs, template):
    if template == "json":
        return render_json(docs)
    else:
        return render_template(docs, template)
