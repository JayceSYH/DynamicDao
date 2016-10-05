# encoding=utf-8
import DynamicDaoCore.exceptions.exceptions as exceptions
from DynamicDaoCore.db_access.db_access import DBAccess
from field import *


class ORM(object):

    def __init__(self, model):
        self.model = model

    def cmd(self, cmd, **kwargs):
        return DBAccess.forward(self.model.access_id, cmd, table=self.model, **kwargs)

    def get(self, **kwargs):
        return self.cmd('get', **kwargs)

    def filter(self, **kwargs):
        return self.cmd('filter', **kwargs)

    def create(self, instance=None, **kwargs):
        if instance is None:
            instance = self.model.instance(**kwargs)
        return self.cmd("create", instance=instance)

    def update(self, instance=None, **kwargs):
        if instance is None:
            instance = self.model.instance(**kwargs)
        return self.cmd("update", instance=instance)

    def create_or_update(self, instance=None, **kwargs):
        if instance is None:
            instance = self.model.instance(**kwargs)
        return self.cmd("create_or_update", instance=instance)

    def sql_query(self, sql):
        return self.cmd("sql_query", sql=sql)


class TableMetaclass(type):

    def __new__(mcs, name, parents, attributes):
        fields_generator = ((key, value) for key, value in attributes.items() if isinstance(value, Field))
        fields = {}

        for key, value in fields_generator:
            value.set_name(key)
            attributes.pop(key)
            fields[key] = value

        attributes['fields'] = fields

        return type.__new__(mcs, name, parents, attributes)

    def __init__(cls, name, parents, attributes):
        super(TableMetaclass, cls).__init__(name, parents, attributes)
        cls.__getitem__ = cls.__getattribute__
        cls.objects = ORM(cls)
        cls.access_id = None

    def __call__(cls, *args, **kwargs):
        instance = super(TableMetaclass, cls).__call__()

        for key, value in cls.fields.items():
            if not value.is_virtual():
                if key in kwargs:
                    setattr(instance, key, value.db_to_python(kwargs[key]))
                else:
                    setattr(instance, key, None)
            else:
                try:
                    setattr(instance, value.virtual_value(instance))
                except Exception:
                    setattr(instance, None)

        return instance


class TableModel(object):
    __metaclass__ = TableMetaclass

    def __getitem__(self, item):
        if item not in self.fields:
            raise exceptions.NoSuchFieldError(self.__class__.__name__, item)

        return getattr(self, item)

    def __repr__(self):
        desc = "<%s>{" % self.__class__.__name__

        start = True
        for key in self.fields:
            add_desc = "'%s':%s" % (key, self[key])
            if start:
                desc += add_desc
                start = False
            else:
                desc += ", %s" % add_desc

        return desc + "}"

    __str__ = __repr__

    def get_db_values(self):
        ret = {}

        for key in self.fields:
            if self.fields[key].is_virtual():
                self.fields[key].virtual_to_db(self[key], self)

            if not self.fields[key].is_auto_increment():
                ret[key] = self.fields[key].python_to_db(self[key])

        return ret

    @classmethod
    def instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)


class DynamicTableModel(TableModel):
    @classmethod
    def add_field(cls, name, field_cls, *args, **kwargs):
        cls.fields[name] = field_cls(*args, **kwargs)

    @classmethod
    def new_class(cls, name, **kwargs):
        return type(name, (DynamicTableModel,), kwargs)
