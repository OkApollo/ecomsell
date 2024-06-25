from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_wtf import FlaskForm
from pymongo import MongoClient 
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, login_required
import random
# Flask-PyMongo
from flask_pymongo import PyMongo
from forms import Registration
from models import userModel as User

# from flask_assets import Bundle, Environment
print(User.get("123"))

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.my_database
collection = db.my_collection
# mongo_pass = "qZVNHnFkg7CjCvH2"

# mongo mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.randint(1000000000, 9999999999))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MONGO_URI'] = client

login_mng = LoginManager(app)
login_mng.login_view = 'login'

@login_mng.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("logsignsite.html")

    user = request.form.get("Username")
    passcode = request.form.get("Password")
    return render_template("main.html", user=user, passcode=passcode)


@app.route("/sp")
def sp():
    return render_template("singleproduct.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        existing_user = User.find_by_email(form.email.data)
        if existing_user is None:
            user = User.create_user(form.username.data, form.email.data, form.password.data)
            flash("Registartion is successfull", "success")
            return redirect(url_for('index'))
        flash("Email already registered", "warning")
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
