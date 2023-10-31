import logging
import traceback

from sqlalchemy import and_

from Flask_FrameMVC.core.Exception.Exceptions import BootException
from Flask_FrameMVC.default.entity.do.Plugin import Session, Plugin, PluginMeta, PluginRouter


class PluginDao:

    def __init__(self):
        self.session = Session()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def arbiter_exist_plugin(self, name, version) -> bool:

        return True if self.session.query(Plugin).join(PluginMeta).filter(
            and_(
                Plugin.name == name,
                PluginMeta.version == version
            )
        ).first() else False

    def get_id_plugin(self, name, version):

        return self.session.query(Plugin).join(PluginMeta).filter(
            and_(
                Plugin.name == name,
                PluginMeta.version == version
            )
        ).first().id

    def create_plugin(
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
        try:
            plugin = Plugin(name=name)
            self.session.add(plugin)

            meta_plugin = PluginMeta(
                plugin_id=plugin.id,
                version=version,
                address=address,
                time_out=time_out if time_out else 0
            )
            self.session.add(meta_plugin)

            router_plugin = PluginRouter(
                plugin_id = plugin.id,
                router_alive=router_alive,
                router_before=router_before,
                router_arbiter_around=router_arbiter_around,
                router_around=router_around,
                router_after=router_after,
                router_after_throwing=router_after_throwing
            )
            self.session.add(router_plugin)

            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise BootException('创建插件失败')

    def update_plugin(
            self,
            id_plugin,
            address=None,
            router_alive=None,
            router_before=None,
            router_arbiter_around=None,
            router_around=None,
            router_after=None,
            router_after_throwing=None,
            version=None,
            time_out=None
    ):
        try:
            plugin_meta = self.session.query(PluginMeta).filter(
                PluginMeta.plugin_id == id_plugin
            )
            plugin_router = self.session.query(PluginRouter).filter(
                PluginRouter.plugin_id == id_plugin
            )

            plugin_meta.info_version = version
            plugin_meta.ip = address
            plugin_meta.time_out = time_out

            plugin_router.alive = router_alive
            plugin_router.before = router_before
            plugin_router.arbiter_around = router_arbiter_around
            plugin_router.around = router_around
            plugin_router.after = router_after
            plugin_router.after_throwing = router_after_throwing

            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise BootException('更新插件失败')

    def logout(self, id_plugin):
        try:
            plugin = self.session.query(Plugin).filter(
                Plugin.id == id_plugin
            ).first()
            plugin.is_activate = False

            self.session.commit()
        except Exception:
            logging.error(traceback.format_exc())
            self.session.rollback()
            raise BootException('注销插件失败')
