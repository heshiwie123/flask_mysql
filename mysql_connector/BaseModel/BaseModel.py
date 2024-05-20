# 基础模型类
class BaseModel:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._original_data = entries.copy()  # 存储原始数据以供后续比较

    @classmethod
    def query(cls, session):
        return Query(cls, session)

    def save(self, session):
        # 初始化用于存储复杂数据类型的列表
        complex_data = {}

        # 构建列名、值和占位符，同时检测复杂数据类型
        columns = []
        values = []
        for key, value in self.__dict__.items():
            print(f"Key: {key}, Value: {value}, Type: {type(value)}")
            if key != 'id':
                if not isinstance(value, (dict, list, set, tuple)):
                    columns.append(key)
                    values.append(value)
                else:
                    # 存储无法直接插入数据库的复杂数据类型
                    complex_data[key] = value

        # 构建占位符
        placeholders = ', '.join(['%s'] * len(values))

        # 检查是否有数据需要插入
        if values:
            query = f"INSERT INTO {self.__tablename__} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor = session.execute(query, tuple(values))
            session.commit()
            return cursor.lastrowid  # 可以返回更具体的信息，比如插入的行ID
        else:
            # 打印复杂类型数据
            if complex_data:
                print("Complex data types detected and not saved:", complex_data)
            return False  # 没有执行插入操作

    def delete(self, session):
        # 确保对象有一个有效的 ID
        if not hasattr(self, 'id') or self.id is None:
            raise ValueError("Cannot delete a record without an ID.")

        try:
            query = f"DELETE FROM {self.__tablename__} WHERE id = %s"
            session.execute(query, (self.id,))
            session.commit()
            return True  # 成功删除
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False

    def update(self, session):
        updates = {}
        for key, value in self.__dict__.items():
            if key not in ['_original_data', 'id'] and self._original_data.get(key) != value:
                updates[key] = value

        if updates:
            update_stmt = ', '.join(f"{key} = %s" for key in updates)
            values = tuple(updates[key] for key in updates)
            query = f"UPDATE {self.__tablename__} SET {update_stmt} WHERE id = %s"
            session.execute(query, values + (self.id,))
            session.commit()
        return self.id


# 查询构建器
class Query:
    def __init__(self, model, session):
        self.model = model
        self.session = session
        self.conditions = []
        self.joins = []
        self.params = []
        self.join_params = []  # 新增存储 join 参数的列表

    def filter(self, condition, *params):
        self.conditions.append(condition)
        self.params.extend(params)
        return self

    def join(self, other_model, on_condition, *params):
        join_statement = f"JOIN {other_model.__tablename__} ON {on_condition}"
        self.joins.append(join_statement)
        if params:
            self.join_params.extend(params)
        return self

    def all(self):
        where_clause = ' AND '.join(self.conditions) if self.conditions else '1=1'
        join_clause = ' '.join(self.joins)
        query = f"SELECT * FROM {self.model.__tablename__} {join_clause} WHERE {where_clause}"
        full_params = self.join_params + self.params
        cursor = self.session.execute(query, full_params)
        result = cursor.fetchall()
        return [self.model(**item) for item in result]

    def first(self):
        results = self.all()
        return results[0] if results else None
