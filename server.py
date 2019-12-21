# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:37:11 2019

@author: Batuhan
"""
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from flask_login import login_user, LoginManager, logout_user
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField
from forms import *
import psycopg2 as dbapi2
import os
import sys
import time
import datetime
from operations import *

#Kullanıcı giriş decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Please login","danger")
            return redirect(url_for("login"))
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisisSecret'
login = LoginManager(app)
url = "postgres://ocponcdw:3qJhgtvyyELu7FXS4FSujJEWJGoYx3V9@raja.db.elephantsql.com:5432/ocponcdw"

@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("index"))
    
@app.route("/userdashboard")
@login_required
def userdashboard():
    user = find_student(session["number"])
    courses = find_courses_inner(user[0])
    if courses != None:
        return render_template("userdashboard.html",courses=courses)
    else: 
        return render_template("userdashboard.html")
    
@app.route("/admindashboard")
@login_required
def admindashboard():
    return render_template("admindashboard.html")

@app.route("/deleteuser")
@login_required
def deleteStudent():
    delete_user_username(session["username"])
    session.clear()
    logout_user()
    return redirect(url_for("index"))

@app.route("/login",methods=["GET","POST"])    
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        number = form.number.data
        password_entered = form.password.data
        result = find_student(number)
        if (result != None):
            data = result         
            real_password = data[5]
            if( sha256_crypt.verify(password_entered,real_password)):     
                flash("Login successfully","success")
                session["logged_in"] = True
                session["number"] = number  # user number
                session["name"] = data[2]   # name of student
                return redirect(url_for("index"))
            else:
                flash("Wrong password","danger")
                return redirect(url_for("login"))
        else:
            flash("User not exists !","danger")
            return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html",form=form)
    return render_template("login.html",form=form)

@app.route("/addStudent",methods=["GET","POST"])
@login_required
def addarticle():
    form = StudentForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        number = form.number.data
        name = form.name.data
        surname = form.surname.data
        grade = form.grade.data
        result = find_student(number)
        if (result == None):
            password = sha256_crypt.encrypt(form.password.data)  
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor() 
                sorgu = "Insert into STUDENT(number,name,surname,grade,password) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(number,name,surname,grade,password)) #tek elemanlıysa (name,)
                connection.commit()
                cursor.close()
                flash("Registered successfully","success") #message,category
                return redirect(url_for("admindashboard"))   
        else:
            flash("Username already exists","warning")
            return render_template("register.html",form = form)
    elif request.method == "GET":   
        return render_template("register.html",form = form)
    else: 
        flash("Unsuccessful operation","warning")
        return render_template("register.html",form = form)

@app.route("/deleteStudent",methods=["GET","POST"])
@login_required
def findStudent():
    if request.method=="GET":
        students = find_students()
        return render_template("deleteStudent.html",students=students)
    else:
        number  = request.form.get("number")
        delete_student(number)
        flash("Deleted successfully","success") #message,category
        return redirect(url_for("admindashboard"))   

@app.route("/deleteTeacher",methods=["GET","POST"])
@login_required
def deleteTeacher():
    if request.method=="GET":
        teachers = find_teachers()
        return render_template("deleteTeacher.html", teachers=teachers)
    else:
        names  = request.form.get("teachername")
        delete_teacher(names)
        flash("Deleted successfully","success") #message,category
        return redirect(url_for("admindashboard")) 

@app.route("/deleteRoom",methods=["GET","POST"])
@login_required
def deleteRoom():
    if request.method=="GET":
        rooms = find_rooms()
        return render_template("deleteRoom.html", rooms=rooms)
    else:
        roomname  = request.form.get("roomname")
        delete_room(roomname)
        flash("Deleted successfully","success") #message,category
        return redirect(url_for("admindashboard")) 

@app.route("/deleteCourse",methods=["GET","POST"])
@login_required
def deleteCourse():
    if request.method=="GET":
        courses = find_courses()
        return render_template("deleteCourse.html", courses=courses)
    else:
        crn  = request.form.get("coursecrn")
        delete_course(crn)
        flash("Deleted successfully","success") #message,category
        return redirect(url_for("admindashboard")) 

@app.route("/")
def index():
    logout_user()
    return render_template("index.html")

@app.route("/addTeacher",methods=["GET","POST"])
@login_required
def addTeacher():
    form = TeacherForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        username = form.username.data
        result = find_teacher(username)
        if result == []:
            flash("Teacher already exists","warning")
            return render_template("registerTeacher.html",form = form)
        name = form.name.data
        surname = form.surname.data 
        coursegiven = form.coursegiven.data
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor() 
            sorgu = "Insert into teacher(username,name,surname,coursegiven) VALUES (%s,%s,%s,%s)"
            cursor.execute(sorgu,(username,name,surname,coursegiven)) #tek elemanlıysa (name,)
            connection.commit()
            cursor.close()
            flash("Teacher Registered successfully","success") #message,category
            return redirect(url_for("admindashboard"))   
    elif request.method == "GET":   
        return render_template("registerTeacher.html",form = form)
    else: 
        flash("Unsuccessful operation","warning")
        return render_template("registerTeacher.html",form = form)

@app.route("/addCourse",methods=["GET","POST"])
@login_required
def addCourse():
    form = Course(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        crn = form.crn.data
        name = form.name.data
        quota = form.quota.data 
        grade = request.form.get("grade")
        day = request.form.get("day")
        starttime = request.form.get("starttime")
        endtime=request.form.get("endtime")

        if grade==None:
           with dbapi2.connect(url) as connection:
                cursor = connection.cursor() 
                sorgu = "Insert into COURSE(crn,name,quota,day,starttime,endtime) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(crn,name,quota,day,int(starttime),int(endtime))) #tek elemanlıysa (name,)
                connection.commit()
                cursor.close()
                flash("Course Registered successfully","success") #message,category
                return redirect(url_for("admindashboard"))  
        else:
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor() 
                sorgu = "Insert into COURSE(crn,name,quota,grade,day,starttime,endtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(crn,name,quota,int(grade),day,int(starttime),int(endtime))) #tek elemanlıysa (name,)
                connection.commit()
                cursor.close()
                flash("Course Registered successfully","success") #message,category
                return redirect(url_for("admindashboard"))   
    elif request.method == "GET":   
        return render_template("registerCourse.html",form = form)
    else: 
        flash("Unsuccessful operation","warning")
        return render_template("registerCourse.html",form = form)

@app.route("/registration",methods=["GET","POST"])
@login_required
def registration():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        user = find_student(session["number"])
        course1 = form.course1.data
        course2 = form.course2.data
        course3 = form.course3.data
         
        result1=find_course(course1)
        result2=find_course(course2)
        result3=find_course(course3)
        if result1 == None: # böyle bir ders var mı
            flash("No course like this","warning") #message,category
            return render_template("registration.html",form = form) 
        else:
            result11= find_course_taker(user[0])
            if (result11 == None):  # dersi almış mı
                flash("You have registered this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result1[3]==0): # derste yer var mı
                flash("No place for this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result1[4]==None): # dersin sınıf koşulu var mı
                register_course(user[0],result1[0])
            elif (result1[4]!=None and user[4]>=result1[4]): # sınıf koşuluna uyuyor mu
                register_course(user[0],result1[0])
            else:
                flash("Registration failed","warning") #message,category
                return render_template("registration.html",form = form)
        
        if result2 == None: # böyle bir ders var mı
            flash("No course like this","warning") #message,category
            return render_template("registration.html",form = form) 
        else:
            result21= find_course_taker(user[0])
            if (result21 == None):  # dersi almış mı
                flash("You have registered this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result2[3]==0): # derste yer var mı
                flash("No place for this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result2[4]==None): # dersin sınıf koşulu var mı
                register_course(user[0],result2[0])
            elif (result2[4]!=None and user[4]>=result2[4]): # sınıf koşuluna uyuyor mu
                register_course(user[0],result2[0])
            else:
                flash("Registration failed","warning") #message,category
                return render_template("registration.html",form = form)
        if result3 == None: # böyle bir ders var mı
            flash("No course like this","warning") #message,category
            return render_template("registration.html",form = form) 
        else:
            result31= find_course_taker(user[0])
            if (result31 == None):  # dersi almış mı
                flash("You have registered this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result3[3]==0): # derste yer var mı
                flash("No place for this course","warning") #message,category
                return render_template("registration.html",form = form)
            elif (result3[4]==None): # dersin sınıf koşulu var mı
                register_course(user[0],result3[0])
            elif (result3[4]!=None and user[4]>=result3[4]): # sınıf koşuluna uyuyor mu
                register_course(user[0],result3[0])
            else:
                flash("Registration failed","warning") #message,category
                return render_template("registration.html",form = form)
        return render_template("index.html")
    else:
        return render_template("registration.html",form = form)


@app.route("/addRoom",methods=["GET","POST"])
@login_required
def addRoom():
    form = Classroom(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        name = form.name.data
        result = find_room(name)
        if result != []:
            flash("Room name exists","warning")
            return render_template("registerRoom.html",form = form)
        quota = form.quota.data 
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor() 
            sorgu = "Insert into CLASSROOM(name,quota) VALUES (%s,%s)"
            cursor.execute(sorgu,(name,quota)) #tek elemanlıysa (name,)
            connection.commit()
            cursor.close()
            flash("Classroom Registered successfully","success") #message,category
            return redirect(url_for("admindashboard"))   
    elif request.method == "GET":   
        return render_template("registerRoom.html",form = form)
    else: 
        flash("Unsuccessful operation","warning")
        return render_template("registerRoom.html",form = form)

@app.route("/optimize")
@login_required
def optimize():
    courses = find_courses_orderby_quota()
    rooms = find_rooms_orderby_quota()
    teachers = find_teachers_orderby_quota()
    i=0
    j=0
    k=0
    while(i<len(courses)):
        j=0
        while(j<len(rooms)):
            if(courses[i][3]<rooms[j][1]):  # ders kontejanı sınıftan küçükse
                start = find_starttime(courses[i][0])
                end = find_endtime(courses[i][0])
                class_course = find_course_from_room(course[i][0])
                if (class_course==None or class_course==[]):    # sınıfa ders atanmamışsa
                    insert_room_for_course(courses[i][0],rooms[j][0])
                    insert_teacher_for_course(courses[i][0],teachers[k][0])
                    k=k+1
                    if(k==len(teachers)):
                        k=0
                    i=i+1
                else:   # atanmışsa saatleri kontrol et uygunsa atama yap
                    start2 = find_course_starttime(courses[i][0],rooms[j][0],courses[i][6])
                    end2 = find_course_endtime(courses[i][0],rooms[j][0],courses[i][6])
                    if ((start<start2 and start<end2 and endz<=start2 and end<end2) or (start>start2 and start>=end2 and end>start2 and end>end2)):
                        insert_room_for_course(courses[i][0],rooms[j][0])
                        insert_teacher_for_course(courses[i][0],teachers[k][0])
                        k=k+1
                        if(k==len(teachers)):
                            k=0
                        i=i+1
                    else:
                        j=j+1
            else:
                j=j+1

@app.route("/rooms")
def rooms():
    rooms = find_rooms()
    if (rooms != None):
        
        return render_template("rooms.html", rooms=rooms)
    else:
        return render_template("rooms.html")

@app.route("/courses")
def courses():
    courses = find_courses()
    if (courses != None):
        
        return render_template("courses.html", courses=courses)
    else:
        return render_template("courses.html")

@app.route("/teachers")
def teachers():
    teachers = find_teachers()
    if (teachers != None):
        
        return render_template("teachers.html", teachers=teachers)
    else:
        return render_template("teachers.html")

@app.route("/students")
def students():
    students = find_students()
    if (students != None):
        return render_template("students.html", students=students)
    else:
        return render_template("students.html")

if __name__ == "__main__":
    app.run(debug=True)


