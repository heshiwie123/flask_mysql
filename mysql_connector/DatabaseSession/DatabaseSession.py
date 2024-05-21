import mysql.connector


# 自定义数据库连接操作
# 用于管理连接connection 和 close
class DatabaseSession:

    def __init__(self, config):  # 构造方法，传入config连接配置
        self.config = config
        self.connection = None

    def open(self):
        self.connection = mysql.connector.connect(**self.config)  # **self.config,自动解包config,否则需要手动取出每一个配置进行设置
        # connection = mysql.connector.connect(
        #     host=self.config['host'],
        #     user=self.config['user'],
        #     password=self.config['password'],
        #     database=self.config['database']
        # )

    def close(self):
        if self.connection:
            self.connection.close()  # 关闭数据库连接，避免浪费资源

    def execute(self, query, params=None): # sql具体执行语句
        if self.connection is None:
            self.open()
        cursor = self.connection.cursor(dictionary=True)    #
        cursor.execute(query, params or ())
        return cursor

    def commit(self):
        if self.connection:
            self.connection.commit()
