"""
Helpers file
"""

import re

from functools import cache


def listify(func):
    """Function to turn the output of a generator to a list."""

    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)

        return list(f)

    return wrapper


@cache
def media(file: str) -> str:
    """Function to read the contents of a file from /media."""

    with open('./media/' + file, 'r') as f:
        return f.read()


def inject(html_str: str, **var_dict) -> str:
    """Function to inject variables into placeholders of an HTML string."""

    for var, value in var_dict.items():
        html_str = re.sub(
            fr'{{%\s*{ var }\s*%}}',
            str(value),
            html_str
        )

    return html_str
