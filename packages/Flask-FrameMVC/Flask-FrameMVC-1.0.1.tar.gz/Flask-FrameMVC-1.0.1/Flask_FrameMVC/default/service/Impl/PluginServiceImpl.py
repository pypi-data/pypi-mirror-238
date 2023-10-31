from Flask_FrameMVC.default.service.PluginServiceInterface import PluginServiceInterface
from Flask_FrameMVC.default.dao.PluginDao import PluginDao


class PluginServiceImpl(PluginServiceInterface):

    def register(
            self,
            name,
            address,
            router_alive,
            router_before,
            router_arbiter_around,
            router_around,
            router_after,
            router_after_throwing,
            version,
            time_out=None
    ):
        with PluginDao() as dao:
            if dao.arbiter_exist_plugin(name, version):
                dao.update_plugin(
                    dao.get_id_plugin(name, version),
                    address,
                    router_alive,
                    router_before,
                    router_arbiter_around,
                    router_around,
                    router_after,
                    router_after_throwing,
                    version,
                    time_out=None
                )
            else:
                dao.create_plugin(
                    name,
                    address,
                    router_alive,
                    router_before,
                    router_arbiter_around,
                    router_around,
                    router_after,
                    router_after_throwing,
                    version,
                    time_out=None
                )

            id_plugin = dao.get_id_plugin(name, version)

        return id_plugin

    def logout(self, name, version):
        with PluginDao() as dao:
            dao.logout(dao.get_id_plugin(name, version))
