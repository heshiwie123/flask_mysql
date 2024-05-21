from mysql_connector.DatabaseSession.DatabaseSession import DatabaseSession
from mysql_connector.Entity.MyModel import Student, Submission, Admin
from mysql_connector.mysql_config.config import db
import datetime
#
# user = Admin(username="admin49", password="123456", phone="12346780", email="456@a.com")
# submission = Submission(lecture_id=1, student_id=2, title="期末作业", submit_time=datetime.datetime.now(),
#                         description="666", is_delete=0)
# result = submission.save(db)  # 保存作业提交
# 结果打印
# print(result)

# 简单查询
users = Student.query(db).filter("username LIKE '方%'").all()  # 获取所有用户名以John开头的用户
for user in users:
    print(user.username + user.password + user.phone)


# 连表查询
submissions = Submission.query(db).join(Student,"student_id = student.id").all()
for submission in submissions:
    # 日期格式转换为字符串,bool可以直接输出
    print(submission.title + submission.submit_time.strftime('%Y-%m-%d %H:%M:%S') + submission.description,
          submission.is_delete)
db.close()
