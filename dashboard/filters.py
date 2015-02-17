def format_mark(value):
    if isinstance(value, dict):
        marks = ''
        for key in value:
            marks += "%s: %s\n" % (key, value[key])
        marks += '\n'
    elif type(value) == str:
        marks = value
    return marks


def format_url(value):
    if len(value) > 50:
        return value[0:15] + '...' + value[-15:]
    return value


def init_app(app):
    """Initialize a Flask application with custom filters."""
    app.jinja_env.filters['format_mark'] = format_mark
    app.jinja_env.filters['format_url'] = format_url
