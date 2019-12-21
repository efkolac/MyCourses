import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    #"DROP TABLE TEACHER",
    #"DROP TABLE CLASSROOM",
    #"DROP TABLE COURSE_TAKERS",
    #"DROP TABLE STUDENT",
    #"DROP TABLE COURSE",
    "CREATE TABLE IF NOT EXISTS STUDENT(id Serial, number char(9) UNIQUE, name varchar(20) NOT NULL, surname varchar(20) NOT NULL, grade Integer NOT NULL, password Text NOT NULL, PRIMARY KEY (id))",
    "CREATE TABLE IF NOT EXISTS COURSE (id Serial, crn CHAR(6) NOT NULL UNIQUE, name varchar(20) NOT NULL, quota Integer NOT NULL, grade Integer, room char(4), day varchar(16),starttime Integer,endtime Integer PRIMARY KEY (id))",
    "CREATE TABLE IF NOT EXISTS CLASSROOM (name varchar(4), quota Integer NOT NULL, PRIMARY KEY(name), FOREIGN KEY(courseId) REFERENCES COURSE(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "CREATE TABLE IF NOT EXISTS COURSE_TAKERS (userId Integer, courseId Integer, PRIMARY KEY(userId, courseId), FOREIGN KEY(userId) REFERENCES STUDENT(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(courseId) REFERENCES COURSE(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "CREATE TABLE IF NOT EXISTS TEACHER (id Serial,username varchar(15) NOT NULL UNIQUE, name varchar(20) NOT NULL, surname varchar(20) NOT NULL, coursegiven Integer, PRIMARY KEY(id))",
    "CREATE TABLE IF NOT EXISTS COURSE_TEACHER (teacherId Integer, courseId Integer, PRIMARY KEY(teacherId, courseId), FOREIGN KEY(teacherId) REFERENCES TEACHER(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(courseId) REFERENCES COURSE(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "CREATE TABLE IF NOT EXISTS COURSE_ROOM (roomname varchar(4), courseId Integer, PRIMARY KEY(roomId, courseId), FOREIGN KEY(roomId) REFERENCES CLASSROOM(name) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(courseId) REFERENCES COURSE(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "INSERT INTO STUDENT (number,name,surname,grade,password) VALUES ('000000000','admin','admin',0,'$5$rounds=535000$Gvb0TNTO7DDGJ.wN$/2NJCFerEVqZrzGF26jZtdngEA0E4Tj0W5zS6TOZfX/')",
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://ocponcdw:3qJhgtvyyELu7FXS4FSujJEWJGoYx3V9@raja.db.elephantsql.com:5432/ocponcdw"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
