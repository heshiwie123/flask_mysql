import mysql.connector
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# 自定义数据库连接操作
# 用于管理连接connection 和 close
from mysql.connector import pooling


class DatabaseSession:
    def __init__(self, config):
        self.pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                                pool_size=10,
                                                **config)
        self.connection = None

    def open(self):
        self.connection = self.pool.get_connection()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    # @contextmanager
    # def cursor(self):
    #     cursor = None
    #     try:
    #         cursor = self.execute("SELECT 1")  # 这里只是为了示例
    #         yield cursor
    #     finally:
    #         if cursor:
    #             cursor.close()

    def execute(self, query, params=None):
        try:
            if self.connection is None:
                self.open()
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
