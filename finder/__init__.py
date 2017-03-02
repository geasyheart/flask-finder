from flask import Flask
from finder import urls
from finder import ext


def create_app():
    app = Flask("finder")
    app.config.from_object('finder.settings')
    app.config.from_envvar('finder', silent=True)
    ext.configure(app)
    urls.configure(app)
    return app
