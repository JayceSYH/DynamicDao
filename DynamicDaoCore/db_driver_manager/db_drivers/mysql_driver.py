# encoding=utf-8


from base_driver import *
import MySQLdb as mysql
import DynamicDaoCore.exceptions.exceptions as exceptions


class MySqlDriver(BaseDBDriver):
    def close(self):
        self.conn.close()

    def begin_transaction(self):
        pass

    def execute_update(self, sql):
        print sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql.encode('utf-8'))
            self.conn.commit()
        except Exception:
            exceptions.print_stack_trace()
            self.conn.rollback()
        finally:
            cursor.close()

    def execute(self, sql):
        print sql
        cursor = self.conn.cursor(cursorclass=mysql.cursors.DictCursor)
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def connect(self, host='host', user='user', password='password', db='database', port=3306, charset='utf8',
                **kwargs):
        return mysql.connect(host=host, user=user, passwd=password, db=db, port=port, charset=charset)

    def get_desc(self, table_name):
        cursor = self.conn.cursor(cursorclass=mysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM %s LIMIT 0" % table_name)
        desc = cursor.description
        cursor.close()
        return {desc[k][0]: MySqlDriver.get_type(desc[k][1]) for k in range(0, len(desc))}

    def get_tables(self):
        tables = self.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='%s' AND table_type='base table'" % self.schema)
        return [t['table_name'].encode("utf-8") for t in tables]

    def add_field(self, table_name, field_name, field_type, prim=False, auto_increment=False):
        sql = "ALTER TABLE `%s` ADD COLUMN `%s` %s" % (table_name, field_name, field_type)
        if auto_increment is True:
            sql += " AUTO_INCREMENT FIRST"
        if prim is True:
            sql += ", ADD PRIMARY KEY(`%s`)" % field_name
        self.execute_update(sql)

    def __init__(self, **kwargs):
        self.conn = self.connect(**kwargs)
        self.schema = kwargs['db']
        print self.get_tables()

    @classmethod
    def init_class(cls):
        field_type = mysql.constants.FIELD_TYPE
        cls.type_dict = {getattr(field_type, k): k for k in dir(field_type) if not k.startswith('_')}

    @staticmethod
    def instance(**kwargs):
        return MySqlDriver(**kwargs)

    @classmethod
    def get_type(cls, type_code):
        if not hasattr(cls, 'type_dict'):
            cls.init_class()
        return cls.type_dict[type_code]

    @staticmethod
    def get_create_fields(fields):
        prim = []
        fields_trim = []

        for key, value in fields.items():
            if value.is_prim():
                prim.append(key)
            field_desc = "`%s` %s" % (key, value.get_type())
            if value.is_auto_increment():
                field_desc += " AUTO_INCREMENT"
            fields_trim.append(field_desc)
        desc = ",".join(fields_trim)

        if len(prim) > 0:
            desc += ', PRIMARY KEY(`%s`)' % ('`,`'.join(prim))

        return desc
