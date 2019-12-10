from flask import Flask, render_template, redirect
from flask import request
import sys
import views

app = Flask(__name__)


# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

@app.route("/")
def admin_page():
    try:
        hospitals = views.get_hospitals()
        print("Rendering...", file=sys.stderr)
    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


@app.route("/doctors")
def doctors_page():
    return render_template('admin_doctors.html')


@app.route("/delete_doctor", methods=['POST'])
def delete_doctor_page():
    doctor_tc = request.form.get("doctor_tc")
    response_for_doctor = views.delete_doctor(doctor_tc)
    return response_for_doctor


if __name__ == "__main__":
    app.debug = True
    app.run()
