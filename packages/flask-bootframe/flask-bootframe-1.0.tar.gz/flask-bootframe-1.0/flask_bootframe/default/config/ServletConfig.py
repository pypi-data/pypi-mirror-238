from flask import Flask

from flask_bootframe.core.Basics import BasicConfig
from flask_bootframe.core.servlet.BootMiddleWare import BootMiddleware


class ServletConfig(BasicConfig):

    def init_app(self, app: Flask):
        app.wsgi_app = BootMiddleware(app.wsgi_app)
