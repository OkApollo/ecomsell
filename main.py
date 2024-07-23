from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_session import Session
from pymongo import MongoClient
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import random
import os
from werkzeug.security import check_password_hash, generate_password_hash
from forms import Registration, LoginForm, AddressAdder, ProductAdder
from models import userModel as User
from models import addressModel as address
from models import productmodel as product
from flask_caching import Cache
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from secrets import token_hex
from admin_decorators import admin_required

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
            try:
                passchecker = User.check_password(user, password=form.password.data)
            except AttributeError:
                raise AttributeError
            if user and passchecker:
                login_user(user)
                session['email'] = form.email.data
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
    if request.method == 'POST' and form.validate_on_submit():
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            filename = secure_filename(file.filename)
            existing_user = User.find_by_email(form.email.data)
            if existing_user is None:
                user = User.create_user(
                    form.username.data, form.email.data, form.password.data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{user._id}.png'))
                flash("Registration is successful", "success")
                login_user(user)
                session['email'] = form.email.data
                return redirect(url_for('home'))
            flash("Email already registered", "warning")
        else:
            flash("No profile picture provided", "warning")
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('email', None)
    flash("You have logged out", "success")
    return redirect(url_for('login'))

@app.route('/userset', methods=["GET", "POST"])
@login_required
def usersettings():
    user = current_user
    addresses = address.find_by_user(user._id)
    return render_template("usersetting.html", user=user)

@app.route('/uploads/<filename>')
def addpfp(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/updatepfp/<id>')
def editpfp():
    pass

@app.route('/address/add', methods=['GET', 'POST'])
@login_required
def address_add():
    form12 = AddressAdder()
    if request.method == "POST" and form12.validate_on_submit():
        address.create_address(current_user._id, form12.country.data, form12.state.data, form12.zipcode.data, form12.note.data)
        flash("Address added successfully", "success")
        return redirect(url_for("addressprofile"))
    return render_template("addressprofile.html")

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
        return redirect(url_for('addressprofile'))
    return redirect(url_for('addressprofile'))

@app.route('/address/delete/<unique_address_id>', methods=['GET'])
@login_required
def address_del(unique_address_id):
    addresses = address.get_from_id(unique_address_id)
    if addresses:
        addresses.delete_from_db()
    return redirect(url_for('addressprofile'))

@app.route("/addressprofile", methods=["POST", "GET"])
@login_required
def addressprofile():
    user = current_user
    address_form = AddressAdder()
    addresses = address.find_by_user(u_id=user._id)
    return render_template("address_content.html", user=user, form=address_form, address=addresses)

@app.route("/purchases", methods=["POST", "GET"])
@login_required
def purchases():
    return render_template("purchases.html", user=current_user)

@app.route("/notifications", methods=["POST", "GET"])
@login_required
def notifications():
    return render_template("notifs.html", user=current_user)

@app.route("/cart", methods=["POST", "GET"])
def cart():
    return render_template("cart.html", user=current_user)





@app.route("/userprofile", methods=["POST", "GET"])
@login_required
def userprofile():
    form12 = Registration(obj=current_user)
    user_id = str(current_user._id)
    if request.method == 'POST' and not form12.validate_on_submit():
        if 'profile_picture' in request.files:
            print("True")
            file = request.files['profile_picture']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}.png'))
        current_user.username = form12.username.data
        current_user.save_to_db()
        flash("Profile updated successfully", "success")
        return redirect(url_for('userprofile'))
    return render_template("userprofile.html", edit_profile_form=form12, user=current_user, user_id=user_id)


# #######################################################

# ADMIN SECTION

@app.route("/addproduct/<PID>", methods=["GET","POST"])
@login_required
@admin_required
def addproduct(PID):
    print(PID)
    return redirect("admin")
    
    

@app.route("/admin", methods=["GET","POST"])
@login_required
@admin_required
def admin():
    form = ProductAdder()
    return render_template("admin.html", form=form)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# @app.route("/admin/dashboard")






if __name__ == "__main__":
    app.run(debug=True)
