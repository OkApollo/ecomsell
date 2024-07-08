from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_wtf import FlaskForm
from pymongo import MongoClient
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import random
# Flask-PyMongo
from werkzeug.security import check_password_hash
from flask_pymongo import PyMongo
from forms import Registration, LoginForm, AddressAdder
from models import userModel as User
from models import addressModel as address
from flask_caching import Cache

# from flask_assets import Bundle, Environment


client = MongoClient(
    "mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.my_database
collection = db.my_collection
# mongo_pass = "qZVNHnFkg7CjCvH2"

# mongo mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.randint(1000000000, 9999999999))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MONGO_URI'] = client
app.config['SESSION_TYPE'] = 'filesystem'

login_mng = LoginManager(app)
login_mng.init_app(app)
login_mng.login_view = 'login'

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/clear_cache')
def clear_cache():
    cache.clear()
    return "Cache cleared"


@login_mng.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            user = User.find_by_email(form.email.data)
            passchecker = User.check_password(
                user, password=form.password.data)
            if user and passchecker:
                print(f"The form:{user._id}")
                # user = User()
                login_user(user)
                flash("Login Successful", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid credentials!", "danger")
        return render_template("logsite.html", form=form)
    else:
        return render_template("logsite.html", form=form)


@app.route("/sp")
@login_required
def sp():
    return render_template("singleproduct.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        existing_user = User.find_by_email(form.email.data)
        if existing_user is None:
            user = User.create_user(
                form.username.data, form.email.data, form.password.data)
            flash("Registartion is successfull", "success")
            login_user(user)
            return redirect(url_for('home'))
        flash("Email already registered", "warning")
        # return render_template(url_redicerct)
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('login'))

# user settings


@app.route('/userset', methods=["GET", "POST"])
@login_required
def usersettings():
    user = current_user
    addresses = address.find_by_user(user._id)
    form = AddressAdder()
    return render_template("usersetting.html", user=user, address=addresses, form = form)

# @app.route('/address/get')
# @login_required
# def address_get():
#     addresses = address.find_by_user(_id=current_user._id)


@app.route('/address/add', methods = ['GET', 'POST'])
@login_required
def address_add():
        form12 = AddressAdder()
        if request.method == "POST":
            print("True")
            if not form12.validate_on_submit():
                addresses = address.create_address(current_user._id, form12.country.data ,form12.state.data, form12.zipcode.data, form12.note.data)
                flash("Address added successfully", "success")
                return redirect(url_for("usersettings"))
        return render_template("singleproduct.html")
        

@app.route('/address/edit/<unique_address_id>', methods = ['GET', 'POST'])
@login_required
def address_edit(unique_address_id):
    addresses = address.get_from_id(unique_address_id)
    form12 = AddressAdder(addresses)
    if not form12.validate_on_submit():
        addresses.country = form12.country.data
        addresses.city = form12.state.data
        addresses.zipcode = form12.zipcode.data
        addresses.notes = form12.note.data
        addresses.save_to_db()
        return redirect(url_for('usersettings'))
    return redirect(url_for('usersettiings'))



@app.route('/address/delete/<unique_address_id>', methods = ['GET', 'POST'])
@login_required
def address_del(unique_address_id):
    form12 = AddressAdder()
    addresses = address()
    addresses.delete_from_db(_id=current_user._id)


if __name__ == "__main__":
    app.run(debug=True)
