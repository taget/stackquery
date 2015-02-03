def format_mark(value):
    if type(value) == type(dict()):
        marks = ''
        for key in value:
            marks += "%s: %s\n" % (key, value[key])
        marks += '\n'
    elif type(value) == str:
        marks = value
    return marks


def init_app(app):
    """Initialize a Flask application with custom filters."""
    app.jinja_env.filters['format_mark'] = format_mark
