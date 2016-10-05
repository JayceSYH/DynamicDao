# encoding=utf-8
from db_access.db_client.db_client import DBClient
from db_access.db_manager.db_manager import DBManager
import config.config_parser as config_parser
import libs.singleton.singleton as singleton


class DynamicDaoCore(singleton.Singleton):
    def __init__(self, config_path):
        # 获取Database Config
        config = config_parser.get_config(config_path)

        # 实例化数据库接口
        if config['access'] == 'manager':
            DBManager(config)
        elif config['access'] == 'client':
            DBClient(config)