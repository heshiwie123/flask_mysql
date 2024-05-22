from mysql_connector.DatabaseSession.DatabaseSession import DatabaseSession

# 数据库的连接配置都在这里，方便修改
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': 'Wei20021016',
          'database': 'stu_instru_management'}
# config = {'host': '127.0.0.1', 'user': 'root', 'password': 'Wei20021016', 'database': 'stu_instru_management'}
# config = {'host': '127.0.0.1', 'user': 'root', 'password': '1234', 'database': 'wad'}
db = DatabaseSession(config)
