import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
origin = ['http://127.0.0.1:3000']
CORS(app, origins=origin)
# 配置数据库的 URI，这里使用 mySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Hello,world!@localhost:3306/stu_instru_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


# 定义模型类，对应数据库中的表
"""管理员表"""


class Admin(SerializerMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))


"""学生表"""


class Student(SerializerMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    major = db.Column(db.String(64))


"""教师表"""


class Instructor(SerializerMixin, db.Model):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    department = db.Column(db.String(16), nullable=False)


"""课程表"""


class Course(SerializerMixin, db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    course_name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256))


"""教课表"""


class Lecture(SerializerMixin, db.Model):
    __tablename__ = 'lecture'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    lecture_name = db.Column(db.String(32))
    course_name = db.Column(db.String(32))
    instructor_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    status = db.Column(db.Integer, default=0)
    is_delete = db.Column(db.Boolean, nullable=False, default=False)


"""学生注册课程表"""


class Enrollment(SerializerMixin, db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # 默认0指未改动
    level = db.Column(db.Integer, nullable=False, default=0)
    academic_year = db.Column(db.String(32), nullable=False)
    # 默认0,指未同意
    condition = db.Column(db.Integer, nullable=False, default=0)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


"""作业表"""


class Assignment(SerializerMixin, db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(32), default='无标题')
    deadline = db.Column(db.DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(days=7))
    description = db.Column(db.UnicodeText)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    is_delete = db.Column(db.Boolean, nullable=False, default=0)


"""学生上交作业表"""


class Submission(SerializerMixin, db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(32))
    submit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    description = db.Column(db.UnicodeText)
    is_delete = db.Column(db.Boolean, nullable=False, default=0)
