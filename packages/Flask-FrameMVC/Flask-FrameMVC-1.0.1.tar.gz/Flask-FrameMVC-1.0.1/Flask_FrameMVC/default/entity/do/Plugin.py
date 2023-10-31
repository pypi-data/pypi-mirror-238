from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, text, sql
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from shortuuid import uuid

Base = declarative_base()
engine = create_engine('sqlite:///resources/sql/plugins.db')
Session = sessionmaker(bind=engine)


class Plugin(Base):
    __tablename__ = 'plugin'

    id = Column("id", String(22), default=uuid, primary_key=True)
    name = Column("name", String(36))
    is_activate = Column("is_activate", Boolean, default=True)


class PluginMeta(Base):
    __tablename__ = 'plugin_meta'

    id = Column("id", String(22), default=uuid, primary_key=True)
    plugin_id = Column('plugin_id', String(22), ForeignKey('plugin.id'))
    version = Column("version", String(36))
    address = Column('address', String(15))
    time_out = Column('time_out', Integer, default=0)
    time_create = Column('time_create', DateTime, server_default=text('CURRENT_TIMESTAMP'), default=sql.func.now())

    source = relationship('Plugin', backref='pluginmeta')

    @hybrid_property
    def info_version(self):

        return self.version

    @info_version.setter
    def info_version(self, value):
        if self.version != value:
            self.version = value

    @hybrid_property
    def ip(self):

        return self.address

    @ip.setter
    def ip(self, value):
        if self.address != value:
            self.address = value
            self.time_create = datetime.now()

    @hybrid_property
    def timeout(self):

        return self.time_out

    @timeout.setter
    def timeout(self, value):
        if self.time_out != value:
            self.time_out = value


class PluginRouter(Base):
    __tablename__ = 'plugin_router'

    id = Column("id", String(22), default=uuid, primary_key=True)
    plugin_id = Column('plugin_id', String(22), ForeignKey('plugin.id'))
    router_alive = Column('router_alive', String(128))
    router_before = Column('router_before', String(128))
    router_arbiter_around = Column('router_arbiter_around', String(128))
    router_around = Column('router_around', String(128))
    router_after = Column('router_after', String(128))
    router_after_throwing = Column('router_after_throwing', String(128))

    source = relationship('Plugin', backref='pluginrouter')

    @hybrid_property
    def alive(self):

        return self.router_alive

    @alive.setter
    def alive(self, value):
        if self.router_alive != value:
            self.router_alive = value

    @hybrid_property
    def before(self):

        return self.router_before

    @before.setter
    def before(self, value):
        if self.router_before != value:
            self.router_before = value

    @hybrid_property
    def arbiter_around(self):

        return self.router_arbiter_around

    @arbiter_around.setter
    def arbiter_around(self, value):
        if self.router_arbiter_around != value:
            self.router_arbiter_around = value

    @hybrid_property
    def around(self):

        return self.router_around

    @around.setter
    def around(self, value):
        if self.router_around != value:
            self.router_around = value

    @hybrid_property
    def after(self):

        return self.router_after

    @after.setter
    def after(self, value):
        if self.router_after != value:
            self.router_after = value

    @hybrid_property
    def after_throwing(self):

        return self.router_after_throwing

    @after_throwing.setter
    def after_throwing(self, value):
        if self.router_after_throwing != value:
            self.router_after_throwing = value


__all__ = [
    'Session',
    'Plugin', 'PluginMeta', 'PluginRouter'
]
