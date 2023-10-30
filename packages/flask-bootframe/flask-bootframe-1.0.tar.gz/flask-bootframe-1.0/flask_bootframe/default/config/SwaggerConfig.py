from flask import Flask
from flasgger import Swagger

from flask_bootframe.core.Basics import BasicConfig


class SwaggerConfig(BasicConfig):
    swagger = None

    def init_app(self, app: Flask):
        self.swagger = Swagger()
        self.swagger.init_app(app)
