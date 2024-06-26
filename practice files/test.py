# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)


# app.config["UPLOAD_FOLDER"] = 'uploads'
# app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# if not os.path.exists(app.config["UPLOAD_FOLDER"]):
#     os.makedirs(app.config["UPLOAD_FOLDER"])


# @app.route("/")
# def index():
#     return "Hello World"


# @app.route("/test")
# def test():
#     return "I am test"

# @app.route("/main", methods=['GET', 'POST'])
# def main():
#     if request.method == 'GET':
#         return render_template("Main.html")
#     else:
#         name = request.form.get("fname")
#         email = request.form.get("email")
#         fileget = request.files.get('file')
#         fileget.save(os.path.join(app.config["UPLOAD_FOLDER"], fileget.filename))
#         return f"{name} {email}"


# @app.route("/test2")
# def test2():
#     return render_template('a1.html')

# @app.route("/runnin")
# def runtest():
#     for i in range(0,10):
#         i+=i
#     return str(i)

# if __name__ == "__main__":
#     app.run(debug=True)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# flash(f"Account created for {form.username.data}!", "success")
#         data = {"name": form.username.data, "email": form.email.data, "password": form.password.data}
#         saved = collection.insert_one(data)
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

from random import 

print(callmemaybe())


