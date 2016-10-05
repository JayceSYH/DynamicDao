# encoding=utf-8
import DynamicDaoCore.exceptions.exceptions as exceptions
from DynamicDaoCore.db_model.field import Field,ViewField
import DynamicDaoCore.db_model.tbl_model as tbl_model


class ORM(object):
    def __init__(self, view):
        self.view = view

    def get(self, **kwargs):
        return self.view.get_view(self.view.model.objects.get(**kwargs))

    def filter(self, **kwargs):
        return map(lambda instance:self.view.get_view(instance), self.view.model.objects.filter(**kwargs))


class ViewMetaclass(type):
    def __new__(mcs, name, parents, attributes):
        fields_generator = ((key, value) for key, value in attributes.items() if isinstance(value, ViewField))
        fields = {}

        for key, value in fields_generator:
            value.set_name(key)
            attributes.pop(key)
            fields[key] = value

        attributes['fields'] = fields

        return type.__new__(mcs, name, parents, attributes)

    def __init__(cls, name, parents, attributes):
        super(ViewMetaclass, cls).__init__(name, parents, attributes)


class TableView(object):

    __metaclass__ = ViewMetaclass

    def __init__(self, cls):
        if not issubclass(cls, tbl_model.TableModel):
            raise exceptions.DynamicDaoException("Argument should be a table model")
        self.model = cls
        self.objects = ORM(self)

    def get_view(self, instance):
        if not instance:
            return None
        if not isinstance(instance, self.model):
            raise exceptions.DynamicDaoException("Model type not matched(object type is '%s'" \
                                                 " but model type is '%s'" % (type(instance).__name__, self.model.__name__))

        view_instance = ViewInstance(self)

        for field in self.fields:
            setattr(view_instance, field, self.fields[field].map_value(instance))

        return view_instance


class ViewInstance(object):
    def __init__(self, view):
        self.__view = view

    def __repr__(self):
        desc = "<%s:%s>{" % (self.__view.__class__.__name__, self.__view.model.__name__)

        start = True
        for key in self.__view.fields:
            add_desc = "'%s':%s" % (key, self[key])
            if start:
                desc += add_desc
                start = False
            else:
                desc += ", %s" % add_desc

        return desc + "}"

    __str__ = __repr__

    def __getitem__(self, item):
        if item not in self.__view.fields:
            raise exceptions.NoSuchFieldError(self.__view.__class__.__name__, item)

        return getattr(self, item)
