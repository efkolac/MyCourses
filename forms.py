from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField, IntegerField
from wtforms.validators import Required,DataRequired
from wtforms.fields.html5 import DateField


class StudentForm(Form):
    number = StringField("Student Number",validators=[validators.length(min=9,max=9)])
    name = StringField("Student Name",validators=[validators.length(min=1)])
    surname = StringField("Student Surname",validators=[validators.length(min=1)])
    grade = IntegerField('Student Grade',validators= [validators.NumberRange(min=1, max=4)])
    password = PasswordField("Password",validators=[validators.DataRequired(message = "Enter a password"),
                            validators.EqualTo(fieldname="confirm",message="Password doesn't match !")])
    confirm = PasswordField("Confirm password")

class TeacherForm(Form):
    username = StringField("Username",validators=[validators.length(min=1)])
    name = StringField("Teacher Name",validators=[validators.length(min=1)])
    surname = StringField("Teacher Surname",validators=[validators.length(min=1)])
    coursegiven = StringField("Avaliable course number",validators=[validators.length(min=1,max=2)])

class RegisterForm(Form):
    course1 = StringField("CRN",validators=[validators.length(max=6)])
    course2 = StringField("CRN",validators=[validators.length(max=6)])
    course3 = StringField("CRN",validators=[validators.length(max=6)])

     
class Classroom(Form):
    name = StringField("Room Name",validators=[validators.length(min=4,max=4)])
    quota = StringField("Quota",validators=[validators.length(min=1)])

class Course(Form):
    crn = StringField("Course CRN",validators=[validators.length(min=6,max=6)])
    name = StringField("Course Name",validators=[validators.length(min=1)])
    quota = StringField("Quota",validators=[validators.length(min=1)])

class LoginForm(Form):
    number = StringField("Student Number")
    password = PasswordField("Password")