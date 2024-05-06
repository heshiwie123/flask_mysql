import datetime
# flask路由，返回json相关
from flask import request, jsonify, Flask, render_template
from sqlalchemy import null
# models中实体类
from entity.model import Admin, Student, Instructor, Course, Enrollment, Assignment, Submission, Lecture, db, app
# 自动化文档
from flasgger import Swagger

Swagger(app)

# 密码加密
from utills import myCheckpw, myBcryptEncoder


# api = Api(app, version='1.0', title='教学 API',
#           description='一个简单的教学管理 API')
#

# 登录
@app.route('/login', methods=['POST'])
def login():
    """
      登录
      ---
      tags:
        - 统一界面
      parameters:
        - name: username
        - name: password
        - name: type
          description: (0:student,1:instructor,2:admin)

      responses:
        500:
          description: Error The language is not awesome!
        200:
          description: A language with its awesomeness
      """
    username = request.form.get('username')
    password = request.form.get('password')
    type = request.form.get('type')
    type = int(type)
    if type == 0:
        # 表名为学生
        user = Student.query.filter(Student.username == username).first()
        print("login学生:=====>" + "username:" + username + "password:" + password)
    if type == 1:
        # 表名为老师
        user = Instructor.query.filter(Instructor.username == username).first()
        print("login教师:=====>" + "username:" + username + "password:" + password)
    if type == 3:
        user = Admin.query.filter(Admin.username == username).first()
        print("login管理:=====>" + "username:" + username + "password:" + password)

    if user:
        # 判断取出的密码是否匹配
        if myCheckpw(password, user.password):
            return jsonify({
                'code': 200,
                'data': {'identity': type},
                'msg': '登录成功'
            })

    return jsonify({
        'code': 500,
        'data': {'res': False},
        'msg': '登录失败,用户名或密码出错'
    })


# 注册
@app.route('/register', methods=['PUT'])
def register():
    """
      注册
      ---
      tags:
        - 统一界面
      parameters:
        - username:
        - password:
        - phone:
        - email:
        - major:
        - department:

      responses:
        500:
          description: Error The language is not awesome!
        200:
          description: A language with its awesomeness
      """
    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')
    email = request.form.get('email')
    major = request.form.get('major')
    department = request.form.get('department')
    type = request.form.get('type')
    type = int(type)
    if type == 0:
        # 表名为学生
        userTest = Student.query.filter(Student.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Student(username=username, password=myBcryptEncoder(password), phone=phone, email=email, major=major)
    if type == 1:
        # 表名为老师
        userTest = Instructor.query.filter(Instructor.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Instructor(username=username, password=myBcryptEncoder(password), phone=phone, email=email,
                          department=department)
    if type == 2:
        # 表名为管理员
        userTest = Admin.query.filter(Admin.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Admin(username=username, password=myBcryptEncoder(password), phone=phone, email=email)

    db.session.add(user)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {'identity': type},
        'msg': '注册成功'
    })


# (获取个人注册课程列表)
@app.route('/course/getByStudentId', methods=['GET'])
def getByStudentId():
    """
        (获取个人注册课程列表)
        ---
        tags:
          - 学生界面
        parameters:
          - student_id:

        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: A language with its awesomeness
        """
    studentId = request.form.get('student_id')
    print("getByStudentId:" + "查询studentId:======>" + studentId)
    # 获取个人选择的教学课程
    enrollmentList = Enrollment.query.filter(Enrollment.student_id == studentId).filter(Enrollment.condition != 0)
    enrollmentLectureIdList = [enrollment.lecture_id for enrollment in enrollmentList]
    # 获取教学课程
    lectureList = Lecture.query.filter(Lecture.id.in_(enrollmentLectureIdList))
    lectureListData = [lecture.to_dict() for lecture in lectureList]
    print(lectureListData)
    # 获取真正课程
    return jsonify({
        'code': 200,
        'data': {'lectureListData': lectureListData},
        'msg': '成功查询'
    })


# (获取教师发布的作业)
@app.route('/assignment/getAssignmentByStudentId', methods=['GET'])
def getAssignmentByStudentId():
    """
        (获取教师发布的作业)
        ---
        tags:
          - 学生界面
        parameters:
          - student_id:

        responses:
          500:
            description:
          200:
            description:
        """
    studentId = request.form.get('student_id')
    print("getAssignmentByStudentId:" + "查询studentId:======>" + studentId)
    # 注册课程列表
    enrollmentList = Enrollment.query.filter(Enrollment.student_id == studentId)
    # enrollmentList = [enrollment.to_dict() for enrollment in enrollmentList]
    enrollmentLectureIdList = [enrollment.lecture_id for enrollment in enrollmentList]
    print(enrollmentLectureIdList)
    # 教学班列表 in查询
    lectureList = Lecture.query.filter(Lecture.id.in_(enrollmentLectureIdList))

    lectureIdList = [lecture.id for lecture in lectureList]

    print(lectureList)
    resultList = []
    for lecture in lectureList:
        assignmentList = Assignment.query.filter(Assignment.lecture_id.in_(lectureIdList))
        # 序列化每一个类
        assignmentList = [assignment.to_dict() for assignment in assignmentList]
        # 作业map, # 教学课程map
        perResult = {'lecture_name': lecture.lecture_name, 'assignmentList': assignmentList}
        resultList.append(perResult)
    # assignmentList = (Assignment.query
    #                   .join(Lecture, Assignment.lecture_id == Lecture.id)
    #                   .join(Enrollment, Enrollment.lecture_id == Lecture.id)
    #                   .join(Student, Enrollment.student_id == Student.id)
    #                   .filter(Student.id == studentId)
    #                   .all())

    return jsonify({
        'code': 200,
        'data': resultList,
        'msg': '成功查询'
    })


# (获取某个课程的教学班列表)
@app.route('/lecture/getAllLectureByCourseId', methods=['GET'])
def getAllLectureByCourseId():
    """
        (获取某个课程的教学班列表)
        ---
        tags:
          - 学生界面
        parameters:
          - course_id:
        responses:
          500:
            description:
          200:
            description:
        """
    courseId = request.form.get('course_id')
    print("getAllLectureByCourseId:" + "查询course_id:======>" + courseId)
    lectureList = Lecture.query.filter(Lecture.course_id == courseId).all()
    lectureListData = [lecture.to_dict() for lecture in lectureList]
    return jsonify({
        'code': 200,
        'data': lectureListData,
        'msg': '成功查询'
    })


# (获取所有课程的教学班列表)
@app.route('/lecture/findAllLecture', methods=['GET'])
def findAllLecture():
    """
    获取所有课程的教学班列表
    ---
    tags:
      - 学生界面
    responses:
      200:
        description: 成功获取所有课程的教学班列表
      500:
        description: 服务器内部错误
    """
    # 所有课程列表
    courseList = Course.query.all()

    # 定义返回结果
    resultList = []
    # 根据课程id批量查询教学课程
    for course in courseList:
        # 课程map
        # courseMap = {'course_name': course.course_name}
        courseId = course.id
        # 查询教学课程
        lectureList = Lecture.query.filter(Lecture.course_id == courseId).all()
        # 序列化每一个类
        lectureListData = [lecture.to_dict() for lecture in lectureList]
        # 教学课程map
        # lectureMap = {'lectureList': lectureListData}
        perResult = {'course_name': course.course_name, 'lectureList': lectureListData}
        resultList.append(perResult)

    return jsonify({
        'code': 200,
        'data': resultList,
        'msg': '成功查询'
    })


# (提交作业)
@app.route('/submission/submitWork', methods=['PUT'])
def submitWork():
    """
        (提交作业)
        ---
        tags:
          - 学生界面
        parameters:
          - student_id:
        responses:
          500:
            description:
          200:
            description:
        """
    lectureId = request.form.get('lecture_id')
    title = request.form.get('title')
    studentId = request.form.get('student_id')
    submit_time = request.form.get('submit_time')
    if submit_time != null and submit_time != ' ' and submit_time is not None:
        submission = Submission(title=title, lecture_id=lectureId, student_id=studentId, submit_time=submit_time)
    else:
        submission = Submission(title=title, lecture_id=lectureId, student_id=studentId)
    db.session.add(submission)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': True,
        'msg': '成功提交'
    })


# (获取作业提交后的状态)
@app.route('/submission/getsubmitWorkByStudentId', methods=['GET'])
def getsubmitWorkByStudentId():
    """
        (获取作业提交后的状态)
        ---
        tags:
          - 学生界面
        parameters:
         - student_id: student_id
        responses:
          500:
            description:
          200:
            description:
        """

    studentId = request.form.get('student_id')

    submissionList = Submission.query.filter(Submission.student_id == studentId).all()

    submissionListData = [submission.to_dict() for submission in submissionList]

    return jsonify({
        'code': 200,
        'data': {'submissionListData': submissionListData},
        'msg': '获取提交状态成功'
    })


# 申请加入课程
@app.route('/enrollment/enterEnrollment', methods=['PUT'])
def enterEnrollment():
    """
        (申请加入课程)
        ---
        tags:
          - 学生界面
        parameters:
          - student_id:
          - lecture_id:
          - academic_year:
        responses:
          500:
            description:
          200:
            description:
        """
    # 教学课程id
    lectureId = request.form.get('lecture_id')
    # level:等级,condition:状态,都有默认值,因为只是学生申请,管理员同意才能修改
    studentId = request.form.get('student_id')
    academicYear = request.form.get('academic_year')

    enrollment = Enrollment(lecture_id=lectureId, student_id=studentId, academic_year=academicYear)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': True,
        'msg': '成功提交'
    })


# 获取所教教学班、课程列表
@app.route('/course/getCourseAndLecture', methods=['GET'])
def getCourseAndLecture():
    """
        (获取个人注册课程列表)
        ---
        tags:
          - 教师界面
        parameters:
          - instructor_id:

        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: A language with its awesomeness
        """
    instructorId = request.form.get('instructor_id')
    print("getCourseAndLecture:" + "查询instructorId:======>" + instructorId)

    # 获取个人所教的教学课程
    lectureList = Lecture.query.filter(Lecture.instructor_id == instructorId).all()
    lectureListData = [lecture.to_dict() for lecture in lectureList]
    # 获取课程

    # 获取真正课程
    return jsonify({
        'code': 200,
        'data': {"lectureListData": lectureListData},
        'msg': '成功查询'
    })


# 获取教学班内学生列表
@app.route('/sutdent/getStudentByInstructorId', methods=['GET'])
def getStudentByInstructorId():
    """
        (获取教学班内学生列表)
        ---
        tags:
          - 教师界面
        parameters:
          - instructor_id:

        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: A language with its awesomeness
        """
    instructorId = request.form.get('instructor_id')
    print("getStudentByInstructorId:" + "查询instructorId:======>" + instructorId)

    # 获取个人所教的教学课程
    lectureList = Lecture.query.filter(Lecture.instructor_id == instructorId).all()

    resultList = []
    for lecture in lectureList:
        # lectureNameMap = {"lecture_name": lecture.lecture_name}
        # 获取教学班得学生列表
        studentList = (Student.query.
                       join(Enrollment, Enrollment.student_id == Student.id).
                       join(Lecture, Lecture.id == Enrollment.lecture_id).
                       filter(Lecture.id == lecture.id).
                       filter(Enrollment.condition != 0).all())

        studentListData = [student.to_dict() for student in studentList]

        # studentListMap = {"studentListData": studentListData}
        # 每个返回map
        perMap = {"lecture_name": lecture.lecture_name, "studentListData": studentListData}

        #    添加到结果
        resultList.append(perMap)
    # 获取真正课程
    return jsonify({
        'code': 200,
        'data': {"lectureListData": resultList},
        'msg': '成功查询'
    })


# (创建教学班)
@app.route('/lecture/createLecture', methods=['PUT'])
def createLecture():
    """
        (创建教学班)
        ---
        tags:
          - 教师界面
        parameters:
          - student_id:
        responses:
          500:
            description:
          200:
            description:
        """
    instructorId = request.form.get('instructor_id')
    courseId = request.form.get('course_id')
    time = request.form.get('time')
    lectureName = request.form.get('lecture_name')
    # 根据课程id获取课程名字
    course = Course.query.filter(Course.id == courseId).first()
    if time != null and time != ' ' and time is not None:
        lecture = Lecture(instructor_id=instructorId, time=time,
                          course_id=courseId, lecture_name=lectureName,
                          course_name=course.course_name)
    else:
        lecture = Lecture(instructor_id=instructorId,
                          course_id=courseId, lecture_name=lectureName,
                          course_name=course.course_name)
    db.session.add(lecture)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': True,
        'msg': '成功创建'
    })


# (创建作业)
@app.route('/assignment/createAssignment', methods=['PUT'])
def createAssignment():
    """
        (创建作业)
        ---
        tags:
          - 教师界面
        parameters:
          - lecture_id:
          - title:
          - deadline:
          - description:
        responses:
          500:
            description:
          200:
            description:
        """
    # 关联得教学课程
    lectureId = request.form.get('lecture_id')
    title = request.form.get('title')
    deadline = request.form.get('deadline')
    description = request.form.get('description')
    # 截至时间若不设置则默认为1星期后
    if deadline != '' and deadline != ' ' and deadline is not None:
        print("传入deadline参数===>{}".format(deadline))
        assignment = Assignment(lecture_id=lectureId, title=title, deadline=deadline, description=description)
    else:
        print("未传入deadline参数")
        assignment = Assignment(lecture_id=lectureId, title=title, description=description)
    db.session.add(assignment)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': True,
        'msg': '成功创建'
    })


# (修改，删除作业)
@app.route('/assignment/updateAssignment', methods=['POST'])
def updateAssignment():
    """
        (修改，删除作业)
        ---
        tags:
          - 教师界面
        parameters:
          - lecture_id:
          - title:
          - deadline:
          - description:
          - is_delete:
        responses:
          500:
            description:
          200:
            description:
        """
    # 关联得教学课程
    id = request.form.get('id')
    lectureId = request.form.get('lecture_id')
    title = request.form.get('title')
    deadline = request.form.get('deadline')
    description = request.form.get('description')
    isDelete = request.form.get('is_delete')
    # 查询特定的 Assignment
    assignment = Assignment.query.filter(Assignment.id == id).first()

    if assignment:
        # 选择性更新字段，只有当相应字段不为空时才更新
        if lectureId:
            assignment.lecture_id = lectureId
        if title:
            assignment.title = title
        if deadline:
            assignment.deadline = deadline
        if description:
            assignment.description = description
        if isDelete:
            assignment.is_delete = bool(isDelete)

        # 提交更新到数据库
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {'res': True},
            'msg': '成功修改'
        })
    else:
        print(" 跟据提供的ID查询不到数据")
        return jsonify({
            'code': 500,
            'data': {'res': '跟据提供的ID查询不到数据,或者没有传id'},
            'msg': '跟据提供的ID查询不到数据,或者没有传id'
        })


# 访问学生的提交作业
@app.route('/submission/getsubmitWorkByInstructorId', methods=['GET'])
def getsubmitWorkByInstructorId():
    """
        (访问学生的提交作业)
        ---
        tags:
          - 教师界面
        parameters:
         - name: student_id
        responses:
          500:
            description:
          200:
            description:
        """

    instructorId = request.form.get('instructor_id')

    lectureList = Lecture.query.filter(Lecture.instructor_id == instructorId).all()
    # 返回结果
    resultList = []

    for lecture in lectureList:
        # 查找每一个教学班对应的作业
        # lectureMap = {'lecture_name': lecture.lecture_name}
        submissionList = Submission.query.filter(Submission.lecture_id == lecture.id).all()
        # 手动序列化,避免无法进行json转换
        submissionListData = [submission.to_dict() for submission in submissionList]
        # submissionListMap = {"submissionListData": submissionListData}

        perResultMap = {'lecture_name': lecture.lecture_name, "submissionListData": submissionListData}

        resultList.append(perResultMap)

    return jsonify({
        'code': 200,
        'data': {"resultList": resultList},
        'msg': '查询成功'
    })


# (评分和提供反馈)
@app.route('/submission/updateSubmission', methods=['POST'])
def updateSubmission():
    """
        (评分和提供反馈)
        ---
        tags:
          - 教师界面
        parameters:
          - id:
          - description:
        responses:
          500:
            description:
          200:
            description:
        """

    id = request.form.get('id')
    description = request.form.get('description')
    # 查询特定的 Assignment
    submission = Submission.query.filter(Submission.id == id).first()

    if submission:
        # 选择性更新字段，只有当相应字段不为空时才更新
        if description:
            submission.description = description

        # 提交更新到数据库
        db.session.commit()
    else:
        print(" 跟据提供的ID查询不到数据")
        return jsonify({
            'code': 500,
            'data': {'res': '跟据提供的ID查询不到数据,或者没有传id'},
            'msg': '跟据提供的ID查询不到数据,或者没有传id'
        })
    return jsonify({
        'code': 200,
        'data': {'res': True},
        'msg': '成功评价'
    })


# 获取用户列表
@app.route('/user/getAllUser', methods=['GET'])
def getAllUser():
    """
        (获取用户列表)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """

    # 查询所有学生
    studentList = Student.query.all()
    studentListData = [student.to_dict() for student in studentList]
    studentListMap = {"studentList": studentListData}
    # 查询所有教师
    instructorList = Instructor.query.all()
    instructorListData = [instructor.to_dict() for instructor in instructorList]
    instructorMap = {"instructorList": instructorListData}
    userList = (studentListMap, instructorMap)
    return jsonify({
        'code': 200,
        'data': userList,
        'msg': '查询成功'
    })


# 创建用户信息
@app.route('/user/addUser', methods=['PUT'])
def addUser():
    """
      创建用户信息
      ---
      tags:
        - 管理员界面
      parameters:
        - username:
        - password:
        - phone:
        - email:
        - major:
        - department:

      responses:
        500:
          description: Error The language is not awesome!
        200:
          description: A language with its awesomeness
      """
    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')
    email = request.form.get('email')
    major = request.form.get('major')
    department = request.form.get('department')
    type = request.form.get('type')
    type = int(type)
    if type == 0:
        # 表名为学生
        userTest = Student.query.filter(Student.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Student(username=username, password=myBcryptEncoder(password), phone=phone, email=email, major=major)
    if type == 1:
        # 表名为老师
        userTest = Instructor.query.filter(Instructor.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Instructor(username=username, password=myBcryptEncoder(password), phone=phone, email=email,
                          department=department)
    if type == 2:
        # 表名为管理员
        userTest = Admin.query.filter(Admin.username == username).first()
        if userTest:
            return jsonify({
                'code': 500,
                'data': {'res': False},
                'msg': '用户已存在，请检查类型或者名字'
            })
        user = Admin(username=username, password=myBcryptEncoder(password), phone=phone, email=email)

    db.session.add(user)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {'identity': type},
        'msg': '注册成功'
    })


# 编辑用户信息
@app.route('/user/editlUser', methods=['POST'])
def editlUser():
    """
        (获取用户列表)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 信息接收
    userId = request.form.get('id')
    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')
    email = request.form.get('email')
    major = request.form.get('major')
    department = request.form.get('department')
    type = request.form.get('type')
    type = int(type)

    if type == 0:
        # 表名为学生
        user = Student.query.filter(Student.id == userId).first()
    if type == 1:
        # 表名为老师
        user = Instructor.query.filter(Instructor.id == userId).first()
    if user:
        # 相同信息
        user.username = username
        user.password = password
        user.phone = phone
        user.email = email
        if major:
            user.major = major
        if department:
            user.department = department
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {"res": True},
            'msg': '编辑成功'
        })
    return jsonify({
        'code': 500,
        'data': {"res": "可能查找不到数据,是否传入id有误"},
        'msg': '可能查找不到数据,是否传入id有误'
    })


# 删除用户信息
@app.route('/user/deleteUser', methods=['DELETE'])
def deleteUser():
    """
        (获取用户列表)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 信息接收
    userId = request.form.get('id')
    type = request.form.get('type')
    if type == 0:
        # 表名为学生
        user = Student.query.filter(Student.id == userId)
    else:
        # 表名为老师
        user = Instructor.query.filter(Instructor.id == userId)
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {"res": True},
        'msg': '删除成功'
    })


# 获取课程列表
@app.route('/course/getAllCourse', methods=['GET'])
def getAllCourse():
    """
        (获取课程列表)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """

    # 查询所有课程
    courseList = Course.query.all()
    courseListData = [course.to_dict() for course in courseList]
    courseListMap = {"courseList": courseListData}

    return jsonify({
        'code': 200,
        'data': courseListMap,
        'msg': '查询成功'
    })


# 创建课程信息
@app.route('/course/addCourse', methods=['PUT'])
def addCourse():
    """
      创建课程信息
      ---
      tags:
        - 管理员界面
      parameters:
        - username:
      responses:
        500:
          description: Error The language is not awesome!
        200:
          description: A language with its awesomeness
      """
    courseName = request.form.get('course_name')
    description = request.form.get('description')
    course = Course(course_name=courseName, description=description)
    db.session.add(course)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {'res': True},
        'msg': '添加成功'
    })


# 编辑课程信息
@app.route('/course/editCourse', methods=['POST'])
def editCourse():
    """
        (编辑课程信息)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 信息接收
    courseId = request.form.get('id')
    courseName = request.form.get('course_name')
    description = request.form.get('description')
    # 根据id查询信息
    course = Course.query.filter(Course.id == courseId).first()
    if course:
        # 修改信息
        if courseName:
            course.course_name = courseName
        if description:
            course.description = description

        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {"res": True},
            'msg': '编辑成功'
        })
    return jsonify({
        'code': 500,
        'data': {"res": "可能查找不到数据,是否传入id有误"},
        'msg': '可能查找不到数据,是否传入id有误'
    })


# 删除课程信息
@app.route('/course/ddeleteCourse', methods=['DELETE'])
def ddeleteCourse():
    """
        (删除课程信息)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 信息接收
    courseId = request.form.get('id')

    # 根据id查询信息
    course = Course.query.filter(Course.id == courseId).first()
    # 修改信息
    db.session.delete(course)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {"res": True},
        'msg': '删除成功'
    })


# 获取教学课程列表
@app.route('/lecture/getAllLecture', methods=['GET'])
def getAllLecture():
    """
        (获取教学课程列表)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """

    # 查询所有教学课程
    lectureList = Lecture.query.all()
    lectureListData = [lecture.to_dict() for lecture in lectureList]
    lectureListMap = {"lectureList": lectureListData}

    return jsonify({
        'code': 200,
        'data': lectureListMap,
        'msg': '查询成功'
    })


# 编辑教学课程信息
@app.route('/lecture/editLecture', methods=['POST'])
def editLecture():
    """
        (编辑教学课程信息)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 获取参数
    lectureId = request.form.get('id')
    time = request.form.get('time')
    lectureName = request.form.get('lecture_name')
    status = request.form.get('status')
    isDelete = request.form.get('is_delete')
    # 查询教学课程
    lecture = Lecture.query.filter(Lecture.id == lectureId).first()

    if lecture:
        if lectureName:
            lecture.lecture_name = lectureName
        if time:
            lecture.time = time
        if status:
            lecture.status = status
        if isDelete:
            lecture.is_delete = bool(isDelete)

        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {"res": True},
            'msg': '编辑成功'
        })

    return jsonify({
        'code': 500,
        'data': {"res": "可能查找不到数据,是否传入id有误"},
        'msg': '可能查找不到数据,是否传入id有误'
    })


# 删除教学课程信息
@app.route('/lecture/deleteLecture', methods=['DELETE'])
def deleteLecture():
    """
        (删除教学课程信息)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 获取参数
    lectureId = request.form.get('id')

    # 查询教学课程
    lecture = Lecture.query.filter(Lecture.id == lectureId).first()

    if lecture:
        db.session.delete(lecture)
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {"res": True},
            'msg': '删除成功'
        })

    return jsonify({
        'code': 500,
        'data': {"res": "可能查找不到数据,是否传入id有误"},
        'msg': '可能查找不到数据,是否传入id有误'
    })


# 为一名教师创建课程
@app.route('/lecture/addLecture', methods=['POST'])
def addLecture():
    """
        (为一名教师管理创建课程)
        ---
        tags:
          - 管理员界面
        responses:
          500:
            description:
          200:
            description:
        """
    # 获取参数
    instructorId = request.form.get('instructor_id')
    courseId = request.form.get('course_id')
    time = request.form.get('time')
    lectureName = request.form.get('lecture_name')
    course = Course.query.filter(Course.id == courseId).first()
    if course:

        if time != '' and time != ' ' and time is not null():
            # 新增教学课程
            lecture = Lecture(instructor_id=instructorId, course_name=course.course_name, course_id=courseId, time=time,
                              lecture_name=lectureName)
        else:
            lecture = Lecture(instructor_id=instructorId, course_name=course.course_name, course_id=courseId,
                              lecture_name=lectureName)
        db.session.add(lecture)
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': {"res": True},
            'msg': '添加成功'
        })
    return jsonify({
        'code': 500,
        'data': {"res": False},
        'msg': '检查一下course_id'
    })


# 决定是否允许学生注册课程
@app.route('/enrollment/decideEnterEnrollment', methods=['POST'])
def decideEnterEnrollment():
    """
        (决定是否允许学生注册课程)
        ---
        tags:
          - 管理员界面
        parameters:
          - id:
          - condition:
        responses:
          500:
            description:
          200:
            description:
        """
    # 教学课程id
    enrollmentId = request.form.get('id')
    print("decideEnterEnrollment:" + "enrollmentId:====>" + enrollmentId)
    # level:等级,condition:状态,都有默认值,因为只是学生申请,管理员同意才能修改
    condition = request.form.get('condition')

    # 查询是否存在
    enrollment = Enrollment.query.filter(Enrollment.id == enrollmentId).first()

    if enrollment:
        enrollment.condition = condition
        print(enrollment)
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': True,
            'msg': '成功提交'
        })
    return jsonify({
        'code': 500,
        'data': False,
        'msg': '检查id'
    })


if __name__ == '__main__':
    # """在第一次请求处理前创建所有定义的表"""
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
