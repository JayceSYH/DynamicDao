# encoding=utf-8

# base ORM functions are implemented in this class --
# including create new row or get a record from database and convert it to object


class BaseORM(object):
    def __init__(self, access_id, driver):
        self.access_id = access_id
        self.driver = driver

    def get_id(self):
        return self.access_id

    def get_model_pool(self):
        pass

    def get_model_by_name(self, name):
        return self.get_model_pool()[name]

    def parse_cmd(self, cmd, **kwargs):
        return getattr(self, cmd)(**kwargs)

    def get(self, **kwargs):
        table = kwargs['table']
        keywords = kwargs
        keywords.pop('table')
        cond = self.get_eq_cond(keywords)
        sql = "SELECT * FROM %s WHERE %s LIMIT 1" % (table.__name__, cond)
        ret = self.driver.execute(sql=sql)
        if len(ret) > 0:
            return table.instance(**(ret[0]))
        else:
            return None

    def filter(self, **kwargs):
        table = kwargs['table']
        keywords = kwargs
        keywords.pop('table')
        cond = self.get_eq_cond(keywords)
        sql = "SELECT * FROM %s WHERE %s" % (table.__name__, cond)
        ret = self.driver.execute(sql=sql)
        if len(ret) > 0:
            return [table.instance(**ret_item) for ret_item in ret]
        else:
            return None

    def create(self, instance, **kwargs):
        table = instance.__class__
        keys = []
        values = []

        for key, value in instance.get_db_values().items():
            keys.append(key)
            values.append(value)

        print table.__name__
        print ','.join(keys)
        print ','.join(values)

        sql = "INSERT INTO %s(%s) VALUES(%s)" % (table.__name__, ','.join(keys), ','.join(values))
        self.driver.execute_update(sql)

    @staticmethod
    def get_eq_cond(keywords):
        cond = ""
        for key, value in keywords.items():
            if value is None:
                add_cond = "%s is null" % key
            else:
                add_cond = "%s=%s" % (key, value)
            if cond != "":
                cond += " AND %s" % add_cond
            else:
                cond += add_cond

        return cond
