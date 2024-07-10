from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_wtf import FlaskForm
from pymongo import MongoClient
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import random
# Flask-PyMongo
import os
from werkzeug.security import check_password_hash
from flask_pymongo import PyMongo
from forms import Registration, LoginForm, AddressAdder
from models import userModel as User
from models import addressModel as address
from flask_caching import Cache
from flask import session, g

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
                # session['user_id'] = user._id # stroing the ID in session.
                if not current_user:
                    flash("Login Successful", "success")
                return redirect(url_for("usersettings"))
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
    user_id = session.get('user_id')
    if user_id is not None:
        logout_user()
        session.pop('user_id', None)
        flash("You have logged out")
    else:
        g.user = None
    return redirect(url_for('login'))

# user settings


@app.route('/userset', methods=["GET", "POST"])
@login_required
def usersettings():
    user = current_user
    addresses = address.find_by_user(user._id)
    # form = AddressAdder()
    # form12 = Registration()
    print(user._id)
    return render_template("usersetting.html", user = user)

# @app.route('/address/get')
# @login_required
# def address_get():
#     addresses = address.find_by_user(_id=current_user._id)

@app.route('/addpfp/<filename>', methods=["GET","POST"])
def addpfp(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
    #id is given correctly
    # another problem - 
    # The selected edit address is giving the first items instead of the items selected to change
    addresses = address.get_from_id(unique_address_id)
    form12 = AddressAdder(obj=addresses)
    if not form12.validate_on_submit():
        addresses.country = form12.country.data
        addresses.city = form12.state.data
        addresses.zipcode = form12.zipcode.data
        addresses.notes = form12.note.data
        addresses.save_to_db()
        return redirect(url_for('usersettings'))
    return redirect(url_for('usersettings'))



@app.route('/address/delete/<unique_address_id>', methods = ['GET'])
@login_required
def address_del(unique_address_id):
    addresses = address.get_from_id(unique_address_id)
    if addresses:
        addresses.delete_from_db()
    return redirect(url_for('usersettings'))



@app.route("/addressprofile", methods= ["POST","GET"])
@login_required
def addressprofile():
    user = current_user
    address_form = AddressAdder()
    addresses = address.find_by_user(u_id=user._id)
    return render_template("address_content.html",user=user, form = address_form, address = addresses)



@app.route("/userprofile", methods = ["POST", "GET"])
@login_required
def userprofile():
    form12 = Registration(obj=current_user)
    user = User(username = current_user.username, email= current_user.email, password_hash=current_user.password_hash, _id = current_user._id)
    if not form12.validate_on_submit():
        user.username = form12.username.data
        user.save_to_db()
        print("validated")
    return render_template("userprofile.html", edit_profile_form = form12, user=current_user)


# @app.route("/userprofile", methods = ["POST", "GET"])
# @login_required
# def userprofile():
#     form12 = Registration(obj=current_user)
#     if not form12.validate_on_submit():
#         current_user.username = form12.username.data
#         current_user.save_to_db()
#         print("saved")
#     return render_template("userprofile.html", edit_profile_form = form12, user=current_user)
    




if __name__ == "__main__":
    app.run(debug=True)
