from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField
from wtforms import StringField, FieldList, SubmitField, FormField, TextField, IntegerField, Label
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, NumberRange
from wtforms.widgets import TextArea
from wtforms.widgets.html5 import NumberInput

from datetime import datetime

class SearchForm(FlaskForm):
    firstname = StringField("Имя: ", validators=[Optional()])
    surname = StringField("Фамилия: ", validators=[Optional()])
    father_name = StringField("Отчество: ", validators=[Optional()])
    date_started = DateField("Дата начала: ", validators=[Optional()])
    date_ended = DateField("Дата завершения: ", validators=[Optional()])
    submit = SubmitField("Поиск")

class GradeForm(Form):
    value = IntegerField("", validators=[Optional()], widget=NumberInput())

class QualificationForm(Form):
    qual_name = StringField("Name: ", validators=[Optional()])
    value = IntegerField("Grade: ", validators=[Optional(), NumberRange (min=0, max=100)], widget=NumberInput())

class GradesTestsForm(FlaskForm):
    testing_min = IntegerField("Проходной балл: ", validators=[Optional()], widget=NumberInput())
    specification = FieldList(StringField("Название раздела: ", validators=[DataRequired()]), min_entries=1)
    tests = FieldList(StringField("Название тестирования: ", validators=[DataRequired()]), min_entries=1)

class NewStudentForm(Form):
    profile_pic = FileField("Фото профиля: ", validators=[Optional()])
    firstname = StringField("Имя: ", validators=[DataRequired()])
    surname = StringField("Фамилия: ", validators=[DataRequired()])
    father_name = StringField("Отчество: ", validators=[Optional()])
    birth_date = DateField("Дата рождения: ", validators=[DataRequired()])
    workplace = StringField("Место работы: ", validators=[Optional()])
    work_experience = StringField("Опыт работы: ", validators=[Optional()])
    phone_number = StringField("Номер телефона: ", validators=[Optional()])
    email = StringField("Электронная почта: ", validators=[Optional()])
    date_started = DateField("Дата начала: ", validators=[Optional()])
    date_ended = DateField("Дата конца: ", validators=[Optional()])

    best = FieldList(FormField(QualificationForm), min_entries=5)
    worst = FieldList(FormField(QualificationForm), min_entries=5)
    grades = FieldList(FormField(GradeForm), min_entries=0)
    tests = FieldList(FormField(GradeForm), min_entries=0)

    problem_points = TextField("Проблемные точки: ", validators=[Optional()], widget=TextArea())
    overall_evaluation = TextField("Общая оценка: ", validators=[Optional()], widget=TextArea())
    recommendations = TextField("Рекомендации для работодателя: ", validators=[Optional()], widget=TextArea())

class StudentForms(FlaskForm):
    forms = FieldList(FormField(NewStudentForm), min_entries=1)
    submit = SubmitField("Добавить")

class CourseForm(FlaskForm):
    name = StringField("Название курса: ", validators=[DataRequired()])
    price = StringField("Цена: ", validators=[Optional()])
    description = TextField("Описание: ", validators=[Optional()], widget=TextArea())
    date_started = DateField("Дата начала: ", validators=[Optional()])
    date_ended = DateField("Дата завершения: ", validators=[Optional()])

    specification = FieldList(StringField("Название раздела: ", validators=[DataRequired()]), min_entries=1)
    tests = FieldList(StringField("Название тестирования: ", validators=[DataRequired()]), min_entries=1)
    testing_min = IntegerField("Проходной балл: ", validators=[Optional()], widget=NumberInput())

    submit = SubmitField("Добавить")