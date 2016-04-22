"""Functions to render the collected documentation to various formats"""

import json
import jinja2
from itertools import groupby


JINJA_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader('lydoc', 'templates'))


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
