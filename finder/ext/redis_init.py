from redis import StrictRedis


class FlaskRedis(object):
    def __init__(self, app=None):
        self._redis_client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        redis_settings = app.config['REDIS_SETTINGS']
        self._redis_client = StrictRedis(**redis_settings)
        return self._redis_client

    def __getattr__(self, method):
        """

            不是太喜欢反射，一旦反射，就不能自动补全了-_-!
        """
        return getattr(self._redis_client, method)


redis_db = FlaskRedis()


def configure(app):
    redis_db.init_app(app)
