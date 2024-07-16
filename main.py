from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from pymongo import MongoClient
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import random
import os
from werkzeug.security import check_password_hash
from forms import Registration, LoginForm, AddressAdder
from models import userModel as User
from models import addressModel as address
from flask_caching import Cache
from werkzeug.utils import secure_filename

# from flask_assets import Bundle, Environment


client = MongoClient(
    "mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.my_database
collection = db.my_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.randint(1000000000, 9999999999))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MONGO_URI'] = client
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'flask:'

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

Session(app)

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
                login_user(user)
                Session['email'] = form.email.data
                flash("Login Successful", "success")
                return redirect(url_for("usersettings"))
            else:
                flash("Invalid credentials!", "danger")
    return render_template("logsite.html", form=form)


@app.route("/sp")
@login_required
def sp():
    return render_template("singleproduct.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
    if request.method == 'POST':
        print(request.files['profile_picture'])
        if not form.validate_on_submit():
            file = request.files['profile_picture']
            filename = secure_filename(file.filename)
            existing_user = User.find_by_email(form.email.data)
            if existing_user is None:
                user = User.create_user(
                    form.username.data, form.email.data, form.password.data)
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], f'{user._id}.png'))
                flash("Registration is successful", "success")
                login_user(user)
                session['email'] = form.email.data
                return redirect(url_for('home'))
            flash("Email already registered", "warning")
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('email', None)
    flash("You have logged out", "success")
    return redirect(url_for('login'))

# @app.route('/admin')
# def admin():
#     user = User()
#     if user.userrole == 1:


@app.route('/userset', methods=["GET", "POST"])
@login_required
def usersettings():
    user = current_user
    addresses = address.find_by_user(user._id)
    return render_template("usersetting.html", user=user)


@app.route('/addpfp/<filename>', methods=["GET", "POST"])
def addpfp(filename):
    return os.send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/address/add', methods=['GET', 'POST'])
@login_required
def address_add():
    form12 = AddressAdder()
    if request.method == "POST":
        if form12.validate_on_submit():
            address.create_address(current_user._id, form12.country.data,
                                   form12.state.data, form12.zipcode.data, form12.note.data)
            flash("Address added successfully", "success")
            return redirect(url_for("usersettings"))
    return render_template("singleproduct.html")


@app.route('/address/edit/<unique_address_id>', methods=['GET', 'POST'])
@login_required
def address_edit(unique_address_id):
    addresses = address.get_from_id(unique_address_id)
    form12 = AddressAdder(obj=addresses)
    if form12.validate_on_submit():
        addresses.country = form12.country.data
        addresses.city = form12.state.data
        addresses.zipcode = form12.zipcode.data
        addresses.notes = form12.note.data
        addresses.save_to_db()
        return redirect(url_for('usersettings'))
    return redirect(url_for('usersettings'))


@app.route('/address/delete/<unique_address_id>', methods=['GET'])
@login_required
def address_del(unique_address_id):
    addresses = address.get_from_id(unique_address_id)
    if addresses:
        addresses.delete_from_db()
    return redirect(url_for('usersettings'))


@app.route("/addressprofile", methods=["POST", "GET"])
@login_required
def addressprofile():
    user = current_user
    address_form = AddressAdder()
    addresses = address.find_by_user(u_id=user._id)
    return render_template("address_content.html", user=user, form=address_form, address=addresses)


@app.route("/userprofile", methods=["POST", "GET"])
@login_required
def userprofile():
    form12 = Registration(obj=current_user)
    if form12.validate_on_submit():
        current_user.username = form12.username.data
        current_user.save_to_db()
        session['user_data']['username'] = current_user.username
        flash("Profile updated successfully", "success")
        return redirect(url_for("usersettings"))
    return render_template("userprofile.html", edit_profile_form=form12, user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
