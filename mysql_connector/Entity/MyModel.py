# 调用自定义的基础模型
import datetime

from mysql_connector.BaseModel.BaseModel import BaseModel


# 公共的序列化方法
class SerializerMixin:

    def to_dict(self, include=None, exclude=None):
        """
        将模型实例转换为字典。

        参数:
        include (list or None): 显式声明要包括的字段。
        exclude (list or None): 显式声明要排除的字段。

        返回:
        dict: 包含模型数据的字典。
        """
        data = {}
        # 获取模型中所有的属性
        attributes = [attr for attr in self.__dict__.keys() if not attr.startswith('_')]
        for attr in attributes:
            # 判断是否应该包含此字段
            if include and attr not in include:
                continue
            if exclude and attr in exclude:
                continue
            # 取出字段的值
            value = getattr(self, attr)
            # 特殊处理日期类型，将其转换为字符串
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = value.isoformat()
            # 添加到字典中
            data[attr] = value
        return data


# 学生实体
class Student(BaseModel, SerializerMixin):
    __tablename__ = 'student'

    # Student 类的构造函数
    # 关键是对应这其父类的 Query.all() [self.model(**item) for item in result]
    # {username: 'Alice', password: 'password123', ...}自动分配到：username, password, phone, email, major,
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

    def __init__(self, course_name, description="", **entries):
        super().__init__(**entries)
        self.course_name = course_name
        self.description = description


# 教学课程实体
class Lecture(BaseModel, SerializerMixin):
    __tablename__ = 'lecture'

    def __init__(self, lecture_name, course_name, instructor_id, course_id, time=datetime.datetime.now(), status=0,
                 academic_year="未安排",
                 is_delete=False, **entries):
        super().__init__(**entries)
        self.time = time
        self.lecture_name = lecture_name
        self.course_name = course_name
        self.instructor_id = instructor_id
        self.academic_year = academic_year
        self.course_id = course_id
        self.status = status
        self.is_delete = is_delete


# 选课记录实体
class Enrollment(BaseModel, SerializerMixin):
    __tablename__ = 'enrollment'

    def __init__(self, academic_year, lecture_id, student_id, level=0, status=0, **entries):
        super().__init__(**entries)
        self.level = level
        self.academic_year = academic_year
        self.status = status
        self.lecture_id = lecture_id
        self.student_id = student_id


# 布置作业实体
class Assignment(BaseModel, SerializerMixin):
    __tablename__ = 'assignment'

    def __init__(self, title, deadline, description, lecture_id, is_delete=False, **entries):
        super().__init__(**entries)
        self.title = title
        self.deadline = deadline
        self.description = description
        self.lecture_id = lecture_id
        self.is_delete = is_delete


# 上交作业实体
class Submission(BaseModel, SerializerMixin):
    __tablename__ = 'submission'

    def __init__(self, title, submit_time, lecture_id, student_id, file_path, description="", is_delete=False,
                 **entries):
        super().__init__(**entries)
        self.title = title
        self.submit_time = submit_time
        self.lecture_id = lecture_id
        self.student_id = student_id
        self.description = description
        self.is_delete = is_delete
        self.file_path = file_path


# 作业反馈实体
class SubmissionFeedBack(BaseModel, SerializerMixin):
    __tablename__ = 'submission_feedback'

    def __init__(self, submission_id, title_information="", score_total=0, score_get=0, provisional_total=0.0,
                 **entries):
        super().__init__(**entries)
        self.submission_id = submission_id
        self.title_information = title_information
        self.score_total = score_total
        self.score_get = score_get
        self.provisional_total = provisional_total


# 作业反馈详情
class SubmissionFeedBackDetail(BaseModel, SerializerMixin):
    __tablename__ = 'feedback_detail'

    def __init__(self, criteria="", comment="", score_sum=0, score_get=0, submission_feedback_id=0.0, **entries):
        super().__init__(**entries)
        self.criteria = criteria
        self.comment = comment
        self.score_sum = score_sum
        self.score_get = score_get
        self.submission_feedback_id = submission_feedback_id
