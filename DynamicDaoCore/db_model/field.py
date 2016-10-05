# encoding=utf-8
import DynamicDaoCore.exceptions.exceptions as exceptions
import datetime


class Field(object):
    db_type = None

    def __repr__(self):
        return self.__class__.__name__

    __str__ = __repr__

    def __init__(self, virtual=False, prim=False, auto_increment=False):
        self.__virtual = virtual
        self.__is_prim = prim
        self.__auto_increment = auto_increment
        self.name = ""

    def python_to_db(self, py_value):
        if self.__is_prim and not py_value:
            raise exceptions.PrimaryKeyIsNullError()
        return py_value

    def db_to_python(self, db_value):
        return db_value

    def set_virtual(self, bl):
        if bl == 1 or bl is True:
            self.__virtual = True
        elif bl == 0 or bl is False:
            self.__virtual = False

    def is_virtual(self):
        return self.__virtual

    def is_prim(self):
        return self.__is_prim is True

    def is_auto_increment(self):
        return self.__auto_increment is True

    def virtual_value(self, table_object):
        pass

    def virtual_to_db(self, virtual_value, table_object):
        pass

    def get_type(self):
        return self.db_type

    def set_name(self, name):
        self.name = name


class ViewField(Field):
    def __init__(self, func=None):
        super(ViewField, self).__init__(virtual=True)
        self.__map_func = func if func is not None else lambda instance: getattr(instance, self.name)

    def map_value(self, instance):
        return self.__map_func(instance)


class StringField(Field):
    def __init__(self, length=255, static=False, *args, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        if not (isinstance(length, int) and length > 0):
            raise exceptions.TypeError('length', type(length))
        if not isinstance(static, bool):
            raise exceptions.TypeError('static', type(static))
        self.db_type = "varchar" if not static else "char"
        self.db_type += "(%d)" % length

    def python_to_db(self, py_value):
        if not py_value:
            if self.is_prim():
                raise exceptions.PrimaryKeyIsNullError(self.name)
            else:
                return "null"
        return "'%s'" % py_value

    def db_to_python(self, db_value):
        return super(StringField, self).db_to_python(db_value).encode('utf-8')


class IntField(Field):
    def __init__(self, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)
        self.db_type = "int"

    def python_to_db(self, py_value):
        py_value = super(IntField, self).python_to_db(py_value)
        if not py_value:
            return "null"
        return "%d" % py_value


class TinyintField(IntField):
    def __init__(self, *args, **kwargs):
        super(TinyintField, self).__init__(*args, **kwargs)
        self.db_type = "tinyint"


class SmallintField(IntField):
    def __init__(self, *args, **kwargs):
        super(SmallintField, self).__init__(*args, **kwargs)
        self.db_type = "smallint"


class BigintField(IntField):
    def __init__(self, *args, **kwargs):
        super(BigintField, self).__init__(*args, **kwargs)
        self.db_type = "bigint"


class DoubleField(Field):
    def __init__(self, *args, **kwargs):
        super(DoubleField, self).__init__(*args, **kwargs)
        self.db_type = "double"


class FloatField(DoubleField):
    def __init__(self, *args, **kwargs):
        super(DoubleField, self).__init__(*args, **kwargs)
        self.db_type = "float"

class DecimalField(Field):
    def __init__(self, total_len=20, float_len=6, *args, **kwargs):
        super(DecimalField, self).__init__(*args, **kwargs)
        if not isinstance(total_len, int):
            exceptions.TypeError("total_len", type(total_len))
        if not isinstance(float_len, int):
            exceptions.TypeError("float_len", type(float_len))
        if total_len <= float_len:
            raise exceptions.DynamicDaoException("total_len must be bigger than float_len")
        self.db_type = "decimal(%d,%d)" % (total_len, float_len)


class DateField(Field):
    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        self.db_type = "date"

    def db_to_python(self, db_value):
        if not isinstance(db_value, datetime.date):
            raise exceptions.TypeError('date', type(db_value))
        return super(DateField, self).db_to_python(db_value)

    def python_to_db(self, py_value):
        if not isinstance(py_value, datetime.date):
            raise exceptions.TypeError("date", type(py_value))
        return py_value


class DatetimeField(Field):
    def __init__(self, *args, **kwargs):
        super(DatetimeField, self).__init__(*args, **kwargs)
        self.db_type = "datetime"

    def db_to_python(self, db_value):
        if not isinstance(db_value, datetime.datetime):
            raise exceptions.TypeError('datetime', type(db_value))
        return super(DatetimeField, self).db_to_python(db_value)

    def python_to_db(self, py_value):
        if not isinstance(py_value, datetime.datetime):
            raise exceptions.TypeError("datetime", type(py_value))
        return py_value


class TimeField(Field):
    def __init__(self, *args, **kwargs):
        super(TimeField, self).__init__(*args, **kwargs)
        self.db_type = "time"

    def db_to_python(self, db_value):
        if not isinstance(db_value, datetime.time):
            raise exceptions.TypeError('time', type(db_value))
        return super(TimeField, self).db_to_python(db_value)

    def python_to_db(self, py_value):
        if not isinstance(py_value, datetime.time):
            raise exceptions.TypeError("time", type(py_value))
        return py_value
