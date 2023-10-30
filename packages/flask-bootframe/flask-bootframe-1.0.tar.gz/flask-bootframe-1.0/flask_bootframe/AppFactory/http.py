from flask import Flask

from flask_bootframe.AppFactory.basic import BasicFactory


class HttpFactory(BasicFactory):

    def __call__(self, name) -> Flask:
        self.app = Flask(name)

        return self.app

    def run(self, *args):
        ...
