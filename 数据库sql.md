### admin(管理员):

```sql
-- auto-generated definition
create table admin
(
    id       int auto_increment
        primary key,
    username varchar(64) charset utf8mb3 not null comment 'username',
    password varchar(64) charset utf8mb3 not null comment 'password',
    phone    varchar(64) charset utf8mb3 null comment 'phone',
    email    varchar(64) charset utf8mb3 null comment 'email'
);
```

### student（学生）

```mysql
-- auto-generated definition
create table student
(
    id       int auto_increment
        primary key,
    username varchar(64) charset utf8mb3 not null comment '用户名',
    password varchar(64) charset utf8mb3 not null comment '密码',
    phone    varchar(64) charset utf8mb3 null comment 'phone',
    email    varchar(64) charset utf8mb3 null comment 'email',
    major    varchar(16) charset utf8mb3 null comment 'major'
);

```

### instructor（教师）

```sql
-- auto-generated definition
create table instructor
(
    id         int auto_increment
        primary key,
    username   varchar(64) charset utf8mb3 not null comment 'username',
    password   varchar(64) charset utf8mb3 not null comment 'password',
    phone      varchar(64) charset utf8mb3 null comment 'phone',
    email      varchar(64) charset utf8mb3 null comment 'email',
    department varchar(16) charset utf8mb3 not null comment 'department'
);
```

### course（课程）

```sql
-- auto-generated definition
create table course
(
    id          int auto_increment
        primary key,
    course_name varchar(32) charset utf8mb3  not null comment 'course_name',
    description varchar(256) charset utf8mb3 null comment 'description'
);
```

### lecture（教师课程）

```sql
-- auto-generated definition
create table lecture
(
    id            int auto_increment
        primary key,
    time          datetime             null comment 'time',
    instructor_id int                  not null comment 'instructor_id ',
    course_id     int                  not null comment 'course_id',
    is_delete     tinyint(1) default 0 not null comment 'is_delete',
    lecture_name  varchar(32)          null,
    course_name   varchar(32)          not null,
    status        int        default 0 not null comment '教课评判状态'
);
```

### enrollment（学生选课记录）

```sql
-- auto-generated definition
create table enrollment
(
    id            int auto_increment comment 'id'
        primary key,
    level         int        default 0        not null comment '"评分等级"',
    academic_year varchar(32) charset utf8mb3 not null comment 'academic_year',
    `condition`   tinyint(1) default 0        not null comment 'condition',
    lecture_id    int                         not null comment 'lecture_id',
    student_id    int                         not null comment '学生id'
);
```

### submission（学生提交作业）

```sql
-- auto-generated definition
create table submission
(
    id          int auto_increment
        primary key,
    lecture_id  int                                  not null comment 'lecture_id',
    student_id  int                                  not null comment 'student_id',
    title       varchar(32) charset utf8mb3          null comment 'title',
    submit_time timestamp  default CURRENT_TIMESTAMP null comment 'submit_time',
    description text                                 null comment 'description',
    is_delete   tinyint(1) default 0                 null comment 'is_delete',
    constraint submission_ibfk_1
        foreign key (lecture_id) references lecture (id),
    constraint submission_student_id_fk
        foreign key (student_id) references student (id)
);

create index lecture_id
    on submission (lecture_id);
```

### assignment(教师布置作业)

```sql
-- auto-generated definition
create table assignment
(
    id          int auto_increment
        primary key,
    lecture_id  int                         null comment 'lecture_id',
    title       varchar(32) charset utf8mb3 null comment 'title',
    deadline    timestamp                   null comment 'deadline',
    description text                        null comment 'description',
    is_delete   tinyint(1) default 0        not null comment 'is_delete',
    constraint assignment_ibfk_1
        foreign key (lecture_id) references lecture (id)
);

create index lecture_id
    on assignment (lecture_id);
```

