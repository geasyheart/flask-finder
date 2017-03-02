from finder.ext import redis_init


def configure(app):
    redis_init.configure(app)
