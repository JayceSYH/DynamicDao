# encoding=utf-8
import traceback


def print_stack_trace():
    traceback.print_exc()


class DynamicDaoException(Exception):
    def __init__(self, desc):
        super(DynamicDaoException, self).__init__()
        self.description = desc

    def __repr__(self):
        return self.description

    __str__ = __repr__


class DatabaseNotSupportedError(DynamicDaoException):
    def __init__(self, database):
        super(DatabaseNotSupportedError, self).__init__("Database '%s' is not supported" % database)


class NoSuchFieldError(DynamicDaoException):
    def __init__(self, table, field):
        super(NoSuchFieldError, self).__init__("No field named '%s' in table '%s'" % (field, table))


class NoSuchAccessError(DynamicDaoException):
    def __init__(self, name):
        super(NoSuchAccessError, self).__init__("No access named '%s'" % name)


class DuplicatedModelError(DynamicDaoException):
    def __init__(self, model_name):
        super(DuplicatedModelError, self).__init__("Duplicated model named '%s'" % model_name)


class PrimaryKeyIsNullError(DynamicDaoException):
    def __init__(self, key_name):
        super(PrimaryKeyIsNullError, self).__init__("Primary key '%s' can not be null" % key_name)


class TypeError(DynamicDaoException):
    def __init__(self, key_name, key_type):
        super(TypeError, self).__init__("Invalid type '%s' for key named '%s'" % (str(key_type), key_name))


class FieldNameError(DynamicDaoException):
    def __init__(self, name):
        super(FieldNameError, self).__init__("Invalid field with build-in name '%s'" % name)
