# encoding=utf-8
import DynamicDaoCore.orm_core.base_orm as base_orm
from DynamicDaoCore.db_model.field import *
from DynamicDaoCore.db_model.tbl_model import DynamicTableModel


class DynamicORM(base_orm.BaseORM):
    field_mapping = {'INT': IntField, 'SHORT': SmallintField, "LONG": BigintField,
                     'DOUBLE': DoubleField, 'FLOAT': FloatField, "DECIMAL": DecimalField, "NEWDECIMAL": DecimalField,
                     "DATE": DateField, "DATETIME": DatetimeField, "TIME": TimeField,
                     "STRING": StringField, "VAR_STRING": StringField}

    def __init__(self, access_id, driver):
        super(DynamicORM, self).__init__(access_id, driver)
        self.model_pool = {}

    def create_mapping(self):
        tables = self.driver.get_tables()
        for table in tables:
            self.mapping_table(table)

    def mapping_table(self, table):
        desc = self.driver.get_desc(table_name=table)
        new_cls = DynamicTableModel.new_class(table)

        for key, value in desc.items():
            new_cls.add_field(key, self.field_mapping[value])

        new_cls.access_id = self.access_id
        self.model_pool[table] = new_cls

    def get_model_by_name(self, name):
        return self.model_pool[name]

    def get_model_pool(self):
        return self.model_pool

    def list_models(self):
        return [key for key in self.model_pool]

    def get_fields(self, model_name):
        return self.model_pool[model_name].fields

