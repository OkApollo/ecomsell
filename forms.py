from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class Registration(FlaskForm):
    username = StringField('Userform', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmpass = PasswordField("Confirm Password", validators=[
                                DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")


# Create it here
class Login(FlaskForm):
    username = StringField("Userform", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Submit")