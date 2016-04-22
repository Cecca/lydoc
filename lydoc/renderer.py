"""Functions to render the collected documentation to various formats"""

import json


def render_json(docs):
    """Represent each doc in docs as a json object, one per line"""
    return "\n".join([json.dumps(doc) for doc in docs]) + "\n"

