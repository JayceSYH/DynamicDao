# encoding=utf-8
from DynamicDaoCore.db_access.db_access import DBAccess
from DynamicDaoCore.orm_core.static_orm.static_orm import StaticORM


class DBManager(DBAccess):

    def __init__(self, conf):
        super(DBManager, self).__init__(conf)
        self.orm_controller = ORMController(conf, self.driver)
        self.orm_controller.mapping_models()

    def parse_cmd(self, cmd, *args, **kwargs):
        return self.orm_controller.parse_cmd(cmd, **kwargs)

    def get_driver(self):
        return self.driver


class ORMController(object):

    def __init__(self, conf, driver):
        self.static_orm = StaticORM(conf['id'], driver)

    def get_instance(self, table_name, **kwargs):
        self.static_orm.get_model_by_name(table_name)(**kwargs)

    def parse_cmd(self, cmd, **kwargs):
        return self.static_orm.parse_cmd(cmd, **kwargs)

    def add_model(self, model):
        self.static_orm.add_model(model)
        self.static_orm.create_mapping()

    def mapping_models(self):
        self.static_orm.create_mapping()


class AccessController(object):
    pass
