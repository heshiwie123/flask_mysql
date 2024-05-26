import mysql.connector
from mysql.connector import pooling
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# 自定义数据库连接操作
# 用于管理连接connection 和 close
class DatabaseSession:

    def __init__(self, config):  # 构造方法，传入config连接配置
        self.pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                                pool_size=30,
                                                **config)  # **self.config,自动解包config,否则需要手动取出每一个配置进行设置
        # connection = mysql.connector.connect(
        #     host=self.config['host'],
        #     user=self.config['user'],
        #     password=self.config['password'],
        #     database=self.config['database']
        # )
        self.connection = None

    def open(self):
        self.connection = self.pool.get_connection()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query, params=None):
        try:
            if self.connection is None:
                self.open()
            #     使用缓冲的游标：使用缓冲游标可以自动读取所有结果到客户端内存中，这样可以防止 Unread result found 错误
            cursor = self.connection.cursor(buffered=True, dictionary=True)
            cursor.execute(query, params or ())
            return cursor
        except Exception as e:
            logger.error("Database execution failed: %s", e)
            if self.connection:
                self.connection.rollback()
            raise

    def commit(self):
        if self.connection:
            self.connection.commit()
