# encoding utf-8
from DynamicDaoCore.core_init import DynamicDaoCore
from DynamicDaoCore.db_access import DBAccess
from DynamicDaoCore.db_model import TableView, ViewField

DynamicDaoCore(config_path='config.xml')


class UserView(TableView):
    id = ViewField()
    desc = ViewField(lambda instance: "name:%s age:%s" % (instance.name, instance.age))


default = DBAccess.get_access()
print default.get_model("userinfo").objects.get(id=1)
user_view = UserView(default.get_model("userinfo"))
instance = user_view.objects.filter(id=1)
print instance
