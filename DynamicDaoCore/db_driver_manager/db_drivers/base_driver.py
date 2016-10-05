# encoding=utf-8


class BaseDBDriver(object):

    # database connect
    def connect(self, host='host', user='user', password='password', db='database', port=3306, charset='utf8'):
        pass

    def close(self):
        pass

    def begin_transaction(self):
        pass

    def execute_update(self, sql):
        pass

    def execute(self, sql):
        pass

    def create_table(self, table_name, fields):
        self.execute_update("CREATE TABLE %s (%s)" % (table_name, self.get_create_fields(fields)))

    def drop_table(self, table_name):
        self.execute_update("DROP TABLE %s" % table_name)

    def truncate_table(self, table_name):
        self.execute_update("TRUNCATE %s" % table_name)

    def delete_field(self, table_name, field_name):
        self.execute_update("ALTER TABLE %s DROP COLUMN %s" % (table_name, field_name))

    def add_field(self, table_name, field_name, field_type, prim=False, auto_increment=False):
        sql = "ALTER TABLE %s ADD COLUMN %s %s" % (table_name, field_name, field_type)
        self.execute_update(sql)

    def get_desc(self, table_name):
        pass

    def get_tables(self):
        pass

    def if_table_exist(self, table_name):
        return table_name in self.get_tables()

    def sql_query(self, table_name, sql):
        return self.execute(sql)

    @classmethod
    def instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @staticmethod
    def get_create_fields(fields):
        prim = []
        fields_trim = []

        for key, value in fields.items():
            if value.is_prim():
                prim.append(key)
            fields_trim.append("%s %s" % (key, value.get_type()))
        desc = ",".join(fields_trim)

        if len(prim) > 0:
            desc += ', PRIMARY KEY(%s)' % (','.join(prim))

        return desc
