import psycopg2 as dbapi2

url = "postgres://ocponcdw:3qJhgtvyyELu7FXS4FSujJEWJGoYx3V9@raja.db.elephantsql.com:5432/ocponcdw"

def find_courses_inner(userid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM COURSE inner join COURSE_TAKERS on courseid = COURSE.id  WHERE userid = %s"
        cursor.execute(sorgu,(userid,))
        user = cursor.fetchall()
        cursor.close()
        return user

def find_courses_orderby_quota():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "select * from course order by quota"
        cursor.execute(sorgu)
        user = cursor.fetchall()
        cursor.close()
        return user

def find_rooms_orderby_quota():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "select * from classroom order by quota"
        cursor.execute(sorgu)
        user = cursor.fetchall()
        cursor.close()
        return user

def insert_room_for_course(courseid,roomname):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor() 
        sorgu = "Update COURSE set room=%s where id = %s "
        cursor.execute(sorgu,(roomname,courseid)) #tek elemanlıysa (name,)
        sorgu = "insert into COURSE_ROOM(roomname,courseId) VALUES (%s,%s) "
        cursor.execute(sorgu,(roomname,courseid)) #tek elemanlıysa (name,)
        connection.commit()
        cursor.close()

def insert_teacher_for_course(courseid,teacherid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor() 
        sorgu = "Insert into COURSE_TEACHER(teacherId,courseId) VALUES (%s,%s)"
        cursor.execute(sorgu,(teacherid,courseid)) #tek elemanlıysa (name,)
        connection.commit()
        cursor.close()

def find_teachers_orderby_quota():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "select * from teacher order by coursegiven desc"
        cursor.execute(sorgu)
        user = cursor.fetchall()
        cursor.close()
        return user        

def find_student(number):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM STUDENT WHERE number = %s"
        cursor.execute(sorgu,(number,))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_course_from_room(courseid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM COURSE_ROOM WHERE courseId = %s"
        cursor.execute(sorgu,(courseid,))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_course_starttime(courseId,roomname,day):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT starttime FROM COURSE inner join COURSE_ROOM on COURSE.id = COURSE_ROOM.courseID WHERE COURSE_ROOM.courseId = %s and COURSE_ROOM.roomname=%s and COURSE.day=%s"
        cursor.execute(sorgu,(courseId,roomname,day))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_starttime(courseId):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT starttime FROM COURSE id = %s"
        cursor.execute(sorgu,(courseId,))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_endtime(courseId):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT endtime FROM COURSE id = %s"
        cursor.execute(sorgu,(courseId,))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_course_endtime(courseId,roomname,day):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT endtime FROM COURSE inner join COURSE_ROOM on COURSE.id = COURSE_ROOM.courseID WHERE COURSE_ROOM.courseId = %s and COURSE_ROOM.roomname=%s and COURSE.day=%s"
        cursor.execute(sorgu,(courseId,roomname,day))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_teacher(username):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM teacher WHERE username = %s"
        cursor.execute(sorgu,(username,))
        user = cursor.fetchone()
        cursor.close()
        return user

def register_course(userid,courseid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor() 
        sorgu = "Insert into COURSE_TAKERS(userId,courseId) VALUES (%s,%s)"
        cursor.execute(sorgu,(userid,courseid)) #tek elemanlıysa (name,)
        sorgu = "Update COURSE set quota = quota-1 where id = %s "
        cursor.execute(sorgu,(userid,courseid)) #tek elemanlıysa (name,)
        connection.commit()
        cursor.close()


def find_course(crn):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM course where crn = %s"
        cursor.execute(sorgu,(crn,))
        courses = cursor.fetchone()
        cursor.close()
        return courses

def find_course_taker(userid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM COURSE_TAKERS where userId = %s"
        cursor.execute(sorgu,(userid,))
        courses = cursor.fetchall()
        cursor.close()
        return courses

def find_students():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM STUDENT"
        cursor.execute(sorgu)
        students = cursor.fetchall()
        cursor.close()
        return students

def find_rooms():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM CLASSROOM"
        cursor.execute(sorgu)
        students = cursor.fetchall()
        cursor.close()
        return students

def find_room(name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM CLASSROOM where name=%s"
        cursor.execute(sorgu,(name,))
        students = cursor.fetchall()
        cursor.close()
        return students

def find_courses():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM course"
        cursor.execute(sorgu)
        students = cursor.fetchall()
        cursor.close()
        return students

def find_teachers():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM teacher"
        cursor.execute(sorgu)
        students = cursor.fetchall()
        cursor.close()
        return students

def delete_student(number):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM student where number = %s"
        cursor.execute(sorgu,(number,))
        cursor.close()

def delete_teacher(username):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM teacher where username = %s"
        cursor.execute(sorgu,(username,))
        cursor.close()

def delete_room(name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM teacher where name = %s"
        cursor.execute(sorgu,(name,))
        cursor.close()

def delete_course(crn):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM course where crn = %s"
        cursor.execute(sorgu,(crn,))
        cursor.close()