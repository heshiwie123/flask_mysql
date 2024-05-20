from mysql_connector.mysql_config.config import MyPackMySQL  # 导入自定义的MySQL包装

# 初始化MySQL类
db = MyPackMySQL('127.0.0.1', 'root', 'Wei20021016', 'stu_instru_management')

# 执行SELECT语句
# db.execute('SELECT * FROM student')
# 获取一个结果

# print(db.fetchone())

# 获取所有结果
# print(db.fetchall())

# 插入新记录
data = {'username': 'user', 'password': '456465', 'email': 'johndoe@example.com'}
db.insert('student', data)

# 更新记录
data = {'username': '小刚'}
condition = "id = 1"
db.update('student', data, condition)

# 删除记录
condition = "id = 10"
db.delete('student', condition)

# 关闭连接
db.close()
