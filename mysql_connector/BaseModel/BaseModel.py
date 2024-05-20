# 基础模型类
class BaseModel:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    @classmethod
    def query(cls, session):
        return Query(cls, session)

    def save(self, session):
        columns = ', '.join([key for key in self.__dict__ if key != 'id'])
        values = tuple(self.__dict__[key] for key in self.__dict__ if key != 'id')
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {self.__tablename__} ({columns}) VALUES ({placeholders})"
        cursor = session.execute(query, values)
        session.commit()
        # 返回新插入的行的ID
        return cursor.lastrowid

    def delete(self, session):
        query = f"DELETE FROM {self.__tablename__} WHERE id = %s"
        session.execute(query, (self.id,))
        session.commit()


# 查询构建器
class Query:
    def __init__(self, model, session):
        self.model = model
        self.session = session
        self.conditions = []
        self.joins = []
        self.params = []

    def filter(self, condition, *params):
        self.conditions.append(condition)
        self.params.extend(params)
        return self

    def join(self, other_model, on_condition):
        join_statement = f"JOIN {other_model.__tablename__} ON {on_condition}"
        self.joins.append(join_statement)
        return self

    def all(self):
        where_clause = ' AND '.join(self.conditions) if self.conditions else '1=1'
        query = f"SELECT * FROM {self.model.__tablename__} WHERE {where_clause}"
        cursor = self.session.execute(query, self.params)
        result = cursor.fetchall()
        return [self.model(**item) for item in result]

    def first(self):
        results = self.all()
        return results[0] if results else None
