# encoding=utf-8
import os
import sys
from DynamicDaoCore.db_model.tbl_model import TableModel
import DynamicDaoCore.orm_core.base_orm as base_orm
import DynamicDaoCore.exceptions.exceptions as exceptions


class StaticORM(base_orm.BaseORM):
    def __init__(self, access_id, conn):
        super(StaticORM, self).__init__(access_id, conn)
        
        model_pool = {}

        package_name = "Models." + access_id
        __import__(package_name)
        table_model_package = sys.modules[package_name]

        package_path = os.path.dirname(table_model_package.__file__)

        for file_name in os.listdir(package_path):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = package_name + '.' + file_name[:-3]
                __import__(module_name)
                _model_module = sys.modules[module_name]

                for module_attr_name in dir(_model_module):
                    module_attr = getattr(_model_module, module_attr_name)
                    if isinstance(module_attr, type) and issubclass(module_attr, TableModel):
                        module_attr.access_id = access_id
                        model_pool[module_attr_name] = module_attr

        self.model_pool = model_pool

    def get_id(self):
        return self.access_id

    def get_model_pool(self):
        return self.model_pool

    def get_model_by_name(self, name):
        return self.model_pool[name]

    def add_model(self, model):
        if model.__name__ in self.model_pool.keys():
            raise exceptions.DuplicatedModelError()
        self.model_pool[model.__name__] = model

    def create_mapping(self):
        for model in self.model_pool.values():
            self.mapping_table(model)

    def mapping_table(self, model):
        if not self.driver.if_table_exist(table_name=model.__name__):
            self.driver.create_table(table_name=model.__name__, fields=model.fields)
        else:
            fields = self.driver.get_desc(table_name=model.__name__)
            for field in model.fields.keys():
                if field not in fields:
                    self.driver.add_field(table_name=model.__name__, field_name=field,
                                          field_type=model.fields[field].get_type(),
                                          prim=model.fields[field].is_prim(),
                                          auto_increment=model.fields[field].is_auto_increment())

