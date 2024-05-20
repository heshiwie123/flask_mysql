# 调用自定义的基础模型
import datetime

from mysql_connector.BaseModel.BaseModel import BaseModel


# 公共的序列化方法
class SerializerMixin:
    def to_dict(self, include=None, exclude=None):
        """将SQLAlchemy模型实例转换为字典。

        参数:
        include (list or None): 显式声明要包括的字段。
        exclude (list or None): 显式声明要排除的字段。

        返回:
        dict: 包含模型数据的字典。
        """
        data = {}
        # 获取模型中所有的列
        for column in self.__table__.columns:
            field_name = column.name
            # 判断是否应该包含此字段
            if include and field_name not in include:
                continue
            if exclude and field_name in exclude:
                continue
            # 取出字段的值
            value = getattr(self, field_name)
            # 特殊处理日期类型，将其转换为字符串
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = value.isoformat()
            data[field_name] = value
        return data


# 学生实体
class Student(BaseModel, SerializerMixin):
    __tablename__ = 'student'

    def __init__(self, username, password, phone, email, major, **entries):
        super().__init__(**entries)
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.major = major


# 管理员实体
class Admin(BaseModel, SerializerMixin):
    __tablename__ = 'admin'

    def __init__(self, username, password, phone, email, **entries):
        super().__init__(**entries)
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email


# 教师实体
class Instructor(BaseModel, SerializerMixin):
    __tablename__ = 'instructor'

    def __init__(self, username, password, phone, email, department, **entries):
        super().__init__(**entries)
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.department = department


# 课程实体
class Course(BaseModel, SerializerMixin):
    __tablename__ = 'course'

    def __init__(self, course_name, description, **entries):
        super().__init__(**entries)
        self.course_name = course_name
        self.description = description


# 教学课程实体
class Lecture(BaseModel, SerializerMixin):
    __tablename__ = 'lecture'

    def __init__(self, time, lecture_name, course_name, instructor_id, course_id, status, is_delete, **entries):
        super().__init__(**entries)
        self.time = time
        self.lecture_name = lecture_name
        self.course_name = course_name
        self.instructor_id = instructor_id
        self.course_id = course_id
        self.status = status
        self.is_delete = is_delete


# 选课记录实体
class Enrollment(BaseModel, SerializerMixin):
    __tablename__ = 'enrollment'

    def __init__(self, level, academic_year, condition, lecture_id, student_id, **entries):
        super().__init__(**entries)
        self.level = level
        self.academic_year = academic_year
        self.condition = condition
        self.lecture_id = lecture_id
        self.student_id = student_id


# 布置作业实体
class Assignment(BaseModel, SerializerMixin):
    __tablename__ = 'assignment'

    def __init__(self, title, deadline, description, lecture_id, is_delete, **entries):
        super().__init__(**entries)
        self.title = title
        self.deadline = deadline
        self.description = description
        self.lecture_id = lecture_id
        self.is_delete = is_delete


# 上交作业实体
class Submission(BaseModel, SerializerMixin):
    __tablename__ = 'submission'

    def __init__(self, title, submit_time, lecture_id, student_id, description, is_delete, **entries):
        super().__init__(**entries)
        self.title = title
        self.submit_time = submit_time
        self.lecture_id = lecture_id
        self.student_id = student_id
        self.description = description
        self.is_delete = is_delete
