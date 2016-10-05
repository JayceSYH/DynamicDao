# encoding=utf-8


import xml.dom.minidom


def get_config(path):
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement

    config = {}

    database = root.getElementsByTagName("database")[0]
    config['type'] = database.getAttribute("type").encode('utf-8')
    config['id'] = database.getAttribute("id").encode('utf-8')
    config['db'] = database.getElementsByTagName('schema')[0].firstChild.data.encode('utf-8')
    config['access'] = database.getElementsByTagName('access')[0].firstChild.data.encode('utf-8')
    config['host'] = database.getElementsByTagName('host')[0].firstChild.data.encode('utf-8')
    config['port'] = int(database.getElementsByTagName('port')[0].firstChild.data)
    config['user'] = database.getElementsByTagName('user')[0].firstChild.data.encode('utf-8')
    config['password'] = database.getElementsByTagName('password')[0].firstChild.data.encode('utf-8')

    return config
