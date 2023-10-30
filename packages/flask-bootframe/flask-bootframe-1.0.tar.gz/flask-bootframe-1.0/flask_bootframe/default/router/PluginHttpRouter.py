from flask_bootframe.core.Basics.interaction import BasicHttpRouter


class PluginHttpRouter(BasicHttpRouter):

    def register(self):
        from flask_bootframe.default.controller.PluginHttpController import PluginHttpController

        self.dict_resource = {
            '/plugin': PluginHttpController
        }
        self.name_bp = __name__
        self.url_prefix = '/sys/side'
