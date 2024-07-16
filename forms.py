from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from pymongo import MongoClient

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/my_database?retryWrites=true&w=majority")

class Registration(FlaskForm):
    profile_picture = FileField('Profile picture', validators=[DataRequired()])
    username = StringField('Userform', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmpass = PasswordField("Confirm Password", validators=[
                                DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")


# Create it here
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddressAdder(FlaskForm):
    country = StringField("country", validators=[DataRequired()])
    state = StringField("state", validators=[DataRequired()])
    zipcode = StringField("zipcode", validators=[DataRequired()])
    note = StringField("note", validators=[DataRequired()])
    submit = SubmitField("Submit")

# class Changeprofile(FlaskForm):
#     username = StringField("Username", validators =)