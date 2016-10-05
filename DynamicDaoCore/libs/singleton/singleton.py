# encoding=utf-8


def empty_func(*args, **kwargs):
    pass


class SingletonMetaclass(type):

    def __call__(cls, *args, **kwargs):
        if hasattr(cls, '_instance'):
            return cls.instance
        else:
            instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
            setattr(cls, 'instance', instance)
            cls.__init__ = empty_func
            return instance


class Singleton(object):
    __metaclass__ = SingletonMetaclass
