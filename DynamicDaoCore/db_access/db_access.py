# encoding=utf-8
import DynamicDaoCore.db_driver_manager.db_driver_manager as db_driver_manager
import DynamicDaoCore.exceptions.exceptions as exceptions


class DBAccess(object):
    access_pool = {}

    @staticmethod
    def connect(conf):
        return db_driver_manager.DBDriverManager.get_driver(conf['type'], conf)

    @classmethod
    def register(cls, access_id, access):
        cls.access_pool[access_id] = access

    @classmethod
    def get_access(cls, access_id="default"):
        try:
            return cls.access_pool[access_id]
        except Exception:
            raise exceptions.NoSuchAccessError(access_id)

    @classmethod
    def forward(cls, access_id, cmd, *args, **kwargs):
        return cls.get_access(access_id).parse_cmd(cmd, *args, **kwargs)

    def __init__(self, conf):
        self.id = conf['id']
        self.driver = self.connect(conf)
        self.register(self.id, self)

    def parse_cmd(self, cmd, *args, **kwargs):
        pass
