"""Contains general template filters and the function that adds template filters to the application"""
from flask import Markup

def html_depth(line, depth=0):
    """Adds appropriate HTML indentation to text strings"""
    indentation = '\t' * depth
    return f"\n{indentation}{line}"


def obj_as_list_of_properties(context_object, depth=0):
    """Returns formatted list of object properties for inspection"""
    output = html_depth('<table border="1">', depth)
    output += html_depth('<tr>', depth + 1)
    output += html_depth('<td>Key</td>', depth + 2)
    output += html_depth('<td>Callable</td>', depth + 2)
    output += html_depth('<td>Result</td>', depth + 2)
    output += html_depth('</tr>', depth + 1)
    for key in dir(context_object):
        if ord(key[0]) < 97 or ord(key[0]) > 122:
            continue
        output += html_depth("<tr>", depth + 1)
        output += html_depth(f"<td>{key}</td>", depth + 2)
        try:
            output += html_depth(
                f"<td>{callable(getattr(context_object, key))}</td>", depth + 2)
        except KeyError:
            output += html_depth(f"<td>False</td>", depth + 2)
        try:
            output += html_depth(
                f"<td>{getattr(context_object, key)()}</td>", depth + 2)
        except (KeyError, TypeError):
            output += html_depth(
                f"<td>{Markup.escape(getattr(context_object, key))}</td>",
                depth + 2
            )
        output += html_depth('</tr>', depth + 1)
    output += html_depth('</table>', depth)
    return Markup(output)


def init_template_filters(app):
    """Adds specifed template filters to the Flask app"""
    app.jinja_env.filters['dir'] = obj_as_list_of_properties
