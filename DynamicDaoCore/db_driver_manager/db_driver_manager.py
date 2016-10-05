# encoding=utf-8
import db_drivers
import DynamicDaoCore.exceptions as exceptions


class DBDriverManager(object):
    __db_mysql = 'MySql'

    def __init__(self, database, conf):
        pass

    @staticmethod
    def get_driver(database, conf):

        driver_type = None
        if database == DBDriverManager.__db_mysql:
            driver_type = db_drivers.mysql_driver.MySqlDriver
        else:
            raise exceptions.DatabaseNotSupportedError(database)

        return DBDriverManager.__connect(driver_type, **conf)

    @staticmethod
    def __connect(driver_type, **kwargs):
        return driver_type.instance(**kwargs)