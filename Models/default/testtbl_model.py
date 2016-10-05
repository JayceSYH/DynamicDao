# encoding utf-8
import DynamicDaoCore.db_model.tbl_model as tbl_model
from DynamicDaoCore.db_model.field import *


class TestTableModel(tbl_model.TableModel):
    name = StringField()
    id = IntField(prim=True, auto_increment=True)


class Test2Model(tbl_model.TableModel):
    id = IntField(prim=True, auto_increment=True)
    name = StringField(length=50)
    decimal = DecimalField(total_len=10, float_len=4)
