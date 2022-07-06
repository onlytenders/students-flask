from flask import render_template, request, redirect, flash, url_for, make_response
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func

from wrapper import app, db
from wrapper.models import Student, User, Course

import uuid as uuid

from wrapper.forms import StudentForms, SearchForm, CourseForm, GradesTestsForm

import os

@app.route('/')
def index():
    return redirect('/student')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')

        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(generate_password_hash(user.password), password):
                login_user(user)

                return redirect('/admin')
            else:
                flash('Login or password is incorrect')
        else:
            flash('Please fill login and password')

    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_page():
    logout_user()
    return redirect('/login')

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    return redirect('/admin/all_students')

@app.route('/admin/all_students', methods=['POST', 'GET'])
@login_required
def all_students():
    search = SearchForm()
    students = Student.query.order_by(Student.id)
    if search.validate_on_submit() and search.data:
        if search.firstname.data:
            students = students.filter(func.lower(Student.name)==search.firstname.data.lower())
        if search.surname.data:
            students = students.filter(func.lower(Student.surname)==search.surname.data.lower())
        if search.father_name.data:
            students = students.filter(func.lower(Student.father_name)==search.father_name.data.lower())
        if search.date_started.data and search.date_ended.data:
            students = students.filter(Student.date_started >= search.date_started.data).filter(Student.date_ended <= search.date_ended.data)
        elif search.date_started.data or search.date_ended.data:
            if search.date_started.data:
                students = students.filter(Student.date_started >= search.date_started.data)
            if search.date_ended.data:
                students = students.filter(Student.date_started <= search.date_ended.data)

        students = students.order_by(Student.id)
    return render_template("admin.html", students=students, search=search)

@app.route('/admin/all_students/<int:id>/edit', methods=["POST", "GET"])
@login_required
def update_student(id):
    student = Student.query.get(id)
    course = Course.query.get(student.course_id)
    students = StudentForms()

    if students.validate_on_submit():
        student.name=students.forms[0].firstname.data
        student.surname=students.forms[0].surname.data
        student.father_name=students.forms[0].father_name.data
        student.birth_date=students.forms[0].birth_date.data
        student.workplace=students.forms[0].workplace.data
        student.work_experience=students.forms[0].work_experience.data
        student.phone_number=students.forms[0].phone_number.data
        student.email=students.forms[0].email.data
        student.date_started=students.forms[0].date_started.data
        student.date_ended=students.forms[0].date_ended.data

        student.best=students.forms[0].best.data
        student.worst=students.forms[0].worst.data

        student.overall_evaluation = students.forms[0].overall_evaluation.data
        student.problem_points = students.forms[0].problem_points.data
        student.recommendations=students.forms[0].recommendations.data

        student.tests = []
        for el in range(0, len(course.tests)):
            student.tests.append({
                'test_name': course.tests[el],
                'test_grade': students.forms[0].tests[el].value.data
            })

        student.grades = []
        for el in range(0, len(course.specification)):
            student.grades.append({
                'course_name': course.specification[el],
                'course_grade': students.forms[0].grades[el].value.data
            })

        if request.files[students.forms[0].profile_pic.name]:
            ending = request.files[students.forms[0].profile_pic.name].filename.split('.')[1]
            old_name = student.profile_pic
            if ending == "png" or ending == "jpg" or ending == "jpeg":
                student.profile_pic=str(uuid.uuid4())+'.'+ending
            else:
                flash("Supported filetypes are jpg, jpeg, png")
                return render_template("update_student.html", students=students, profile_pic=profile_pic)

            if old_name:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_name))

            image_data = request.files[students.forms[0].profile_pic.name].read()
            open(os.path.join(app.config['UPLOAD_FOLDER'], student.profile_pic), 'wb').write(image_data)


        try:
            db.session.commit()
        except:
            flash("Error")

        return redirect('/admin')

    students.forms[0].firstname.data=student.name
    students.forms[0].surname.data=student.surname
    students.forms[0].father_name.data=student.father_name
    students.forms[0].birth_date.data=student.birth_date
    students.forms[0].workplace.data=student.workplace
    students.forms[0].work_experience.data=student.work_experience
    students.forms[0].phone_number.data=student.phone_number
    students.forms[0].email.data=student.email
    students.forms[0].date_started.data=student.date_started
    students.forms[0].date_ended.data=student.date_ended

    for el in course.specification:
        students.forms[0].grades.append_entry()
    for el in course.tests:
        students.forms[0].tests.append_entry()

    for el in range(0, len(student.grades)):
        students.forms[0].grades[el].value.data = student.grades[el]['course_grade']
    for el in range(0, len(student.tests)):
        students.forms[0].tests[el].value.data = student.tests[el]['test_grade']

    for el in range(0, len(students.forms[0].best)):
        if student.best[el]['qual_name']:
            students.forms[0].best[el].qual_name.data = student.best[el]['qual_name']
        if student.best[el]['value']:
            students.forms[0].best[el].value.data = student.best[el]['value']

    for el in range(0, len(students.forms[0].worst)):
        if student.worst[el]['qual_name']:
            students.forms[0].worst[el].qual_name.data = student.worst[el]['qual_name']
        if student.worst[el]['value']:
            students.forms[0].worst[el].value.data = student.worst[el]['value']

    students.forms[0].overall_evaluation.data = student.overall_evaluation
    students.forms[0].problem_points.data = student.problem_points
    students.forms[0].recommendations.data=student.recommendations

    profile_pic = 'No profile pic yet, you can upload one: '
    if student.profile_pic:
        profile_pic = 'Update a profile pic: '

    return render_template("update_student.html", students=students, profile_pic=profile_pic, course=course, student=student)

@app.route('/admin/all_students/<int:id>/delete')
@login_required
def delete_student(id):
    student = Student.query.get(id)

    if student.profile_pic:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], student.profile_pic))

    try:
        db.session.delete(student)
        db.session.commit()
        return redirect('/admin')
    except:
        return make_response("Error")

@app.route('/admin/courselist', methods=['GET', 'POST'])
@login_required
def courselist():
    courses = Course.query.order_by(Course.id)
    return render_template('courselist.html', courses=courses)

@app.route('/admin/courselist/<int:id>')
@login_required
def course(id):
    course = Course.query.get(id)
    students = Student.query.filter(Student.course_id==course.id).order_by(Student.id)
    return render_template('course.html', course=course, students=students)

@app.route('/admin/courselist/<int:id>/delete')
@login_required
def delete_course(id):
    course = Course.query.get(id)
    try:
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('courselist'))
    except:
        return make_response("Error")

@app.route('/admin/courselist/<int:course_id>/add_new_student', methods=['GET', 'POST'])
@login_required
def add_new_student(course_id):
    students = StudentForms()
    course = Course.query.get(course_id)

    if students.validate_on_submit():
        for student in students.forms:
            to_add = Student(
                name=student.firstname.data,
                surname=student.surname.data,
                father_name=student.father_name.data,
                birth_date=student.birth_date.data,
                workplace=student.workplace.data,
                work_experience=student.work_experience.data,
                phone_number=student.phone_number.data,
                email=student.email.data,
                date_started=student.date_started.data,
                date_ended=student.date_ended.data,

                tests = [],
                grades = [],
                best = student.best.data,
                worst = student.worst.data,

                overall_evaluation = student.overall_evaluation.data,
                problem_points = student.problem_points.data,
                recommendations = student.recommendations.data,
                profile_pic='',
                hash=str(uuid.uuid4()),
                course_id = course.id
            )

            for el in range(0, len(course.tests)):
                to_add.tests.append({
                    'test_name': course.tests[el],
                    'test_grade': student.tests[el].value.data
                })

            for el in range(0, len(course.specification)):
                to_add.grades.append({
                    'course_name': course.specification[el],
                    'course_grade': student.grades[el].value.data
                })

            if request.files[student.profile_pic.name]:
                ending = request.files[student.profile_pic.name].filename.split('.')[1]

                if ending == "png" or ending == "jpg" or ending == "jpeg":
                    to_add.profile_pic=str(uuid.uuid4())+'.'+ending
                else:
                    flash("Supported filetypes are jpg, jpeg, png")
                    return render_template("add_student.html", students=students, course=course)

            try:
                db.session.add(to_add)
            except:
                flash("Error")

            if request.files[student.profile_pic.name] and not to_add.profile_pic == '':
                image_data = request.files[student.profile_pic.name].read()
                open(os.path.join(app.config['UPLOAD_FOLDER'], to_add.profile_pic), 'wb').write(image_data)

        try:
            db.session.commit()
        except:
            flash("Error")

        return redirect('/admin')

    if students.errors:
        return students.data

    for el in course.specification:
        students.forms[0].grades.append_entry()
    for el in course.tests:
        students.forms[0].tests.append_entry()
    return render_template("add_student.html", students=students, course=course)

@app.route('/admin/add_new_course', methods=['GET', 'POST'])
@login_required
def add_new_course():
    course = CourseForm()
    if course.validate_on_submit():
        new_course = Course(
            name = course.name.data,
            price = course.price.data,
            description = course.description.data,
            date_started = course.date_started.data,
            date_ended = course.date_ended.data,
            specification = course.specification.data,
            tests = course.tests.data,
            testing_min = course.testing_min.data
        )

        try:
            db.session.add(new_course)
            db.session.commit()
        except:
            flash("Error")
        return redirect(url_for('courselist'))
    if course.data and course.errors:
        return course.data
    return render_template('add_new_course.html', form=course)

@app.route('/admin/courselist/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    form = CourseForm()
    course = Course.query.get(course_id)
    students = Student.query.filter(Student.course_id==course_id).order_by(Student.id)

    if form.validate_on_submit():
        course.name = form.name.data
        course.price = form.price.data
        course.description = form.description.data
        course.date_started = form.date_started.data
        course.date_ended = form.date_ended.data

        course.specification = form.specification.data
        course.tests = form.tests.data
        course.testing_min = form.testing_min.data

        try:
            db.session.commit()
        except:
            flash("Something is wrong")
            return render_template('edit_course.html', form=form, course=course)

        return redirect(url_for('courselist'))

    while not len(course.specification) == len(form.specification):
        form.specification.append_entry()
    while not len(course.tests) == len(form.tests):
        form.tests.append_entry()
    return render_template('edit_course.html', form=form, course=course)

@app.route('/admin/courselist/<int:course_id>/edit/spec', methods=['GET', 'POST'])
@login_required
def edit_course_spec(course_id):
    course = Course.query.get(course_id)
    form = GradesTestsForm()

    if form.validate_on_submit():
        course.specification=form.specification.data
        course.tests=form.tests.data
        course.testing_min=form.testing_min.data

        students = Student.query.filter(Student.course_id==course_id).order_by(Student.id)
        for student in students:
            if len(course.specification) > len(student.grades):
                student.grades.append({'course_name' : course.specification[-1], 'course_grade' : None})
            if len(course.specification) < len(student.grades):
                yes = False
                for i in range(0,len(course.specification)):
                    if not student.grades[i]['course_name'] == course.specification[i]:
                        student.grades.pop(i)
                        yes = True
                        break
                if not yes:
                    student.grades.pop()

            if len(course.tests) > len(student.tests):
                student.tests.append({'test_name' : course.tests[-1], 'test_grade' : None})
            if len(course.tests) < len(student.tests):
                yes = False
                for i in range(0,len(course.tests)):
                    if not student.tests[i]['test_name'] == course.tests[i]:
                        student.tests.pop(i)
                        yes = True
                        break
                if not yes:
                    student.tests.pop()

        try:
            db.session.commit()
        except:
            flash("Something is wrong")
            return render_template('edit_course_spec.html', form=form, course=course)

    course = Course.query.get(course_id)

    while not len(course.specification) == len(form.specification):
        if len(form.specification) > len(course.specification):
            form.specification.pop_entry()
        if len(form.specification) < len(course.specification):
            form.specification.append_entry()
    while not len(course.tests) == len(form.tests):
        if len(form.tests) > len(course.tests):
            form.tests.pop_entry()
        if len(form.tests) < len(course.tests):
            form.tests.append_entry()

    return render_template('edit_course_spec.html', form=form, course=course)

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == "POST":
        hash = request.form['hash']
        return redirect('/student/' + hash)
    else:
        return render_template("student.html")

@app.route('/student/<string:hash>')
def student_evaluation(hash):
    student = Student.query.filter_by(hash=hash).first_or_404()
    course = Course.query.filter_by(id=student.course_id).first_or_404()
    return render_template("evaluation.html", student=student, course=course)

@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    elif response.status_code == 404:
        return make_response("Page not found")
    else:
        return response