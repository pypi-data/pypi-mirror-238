from Flask_FrameMVC.core.Basics.interaction import BasicHttpRouter


class PluginHttpRouter(BasicHttpRouter):

    def register(self):
        from Flask_FrameMVC.default.controller.PluginHttpController import PluginHttpController

        self.dict_resource = {
            '/plugin': PluginHttpController
        }
        self.name_bp = __name__
        self.url_prefix = '/sys/side'
