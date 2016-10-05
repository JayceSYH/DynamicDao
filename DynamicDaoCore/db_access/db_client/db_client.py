# encoding=utf-8
import DynamicDaoCore.db_driver_manager.db_driver_manager as db_driver_manager
from DynamicDaoCore.db_access.db_access import DBAccess
import DynamicDaoCore.orm_core.dynamic_orm.dynamic_orm as dynamic_orm


class DBClient(DBAccess):

    def __init__(self, config):
        super(DBClient, self).__init__(config)
        self.orm_controller = ORMController(config, self.driver)
        self.orm_controller.mapping_models()

    def list_models(self):
        return self.orm_controller.list_models()

    def get_fields(self, model_name):
        return self.orm_controller.get_fields(model_name)

    def get_driver(self):
        return self.driver

    def get_model(self, name):
        return self.orm_controller.get_model(name)

    def get_instance(self, name, **kwargs):
        return self.orm_controller.get_instance(model=name, **kwargs)

    def parse_cmd(self, cmd, **kwargs):
        return self.orm_controller.parse_cmd(cmd, **kwargs)


class ORMController(object):
    def __init__(self, conf, driver):
        self.dynamic_orm = dynamic_orm.DynamicORM(conf['id'], driver)

    def get_instance(self, model, **kwargs):
        self.dynamic_orm.get_model_by_name(model)(**kwargs)

    def mapping_models(self):
        self.dynamic_orm.create_mapping()

    def list_models(self):
        return self.dynamic_orm.list_models()

    def get_fields(self, model_name):
        return self.dynamic_orm.get_fields(model_name)

    def get_model(self, name):
        return self.dynamic_orm.get_model_by_name(name)

    def parse_cmd(self, cmd, **kwargs):
        return self.dynamic_orm.parse_cmd(cmd, **kwargs)