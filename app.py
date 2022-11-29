from flask import Flask, render_template, request, flash, url_for, session, redirect, send_from_directory, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from ocr import *
from db import Mongo
import os
import hashlib

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'pdf')
UPLOAD_FOLDER = '../OCR_FILES/'

app = Flask(__name__)
app.secret_key = "alphafst"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowedFileExtension(filename):
    fileExt = filename.split(".")[1].lower()
    if fileExt in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        formData = request.form
        password = formData['password'].encode()
        hashed_password = hashlib.md5(password)

        mongo = Mongo()
        user = mongo.getUsersByUsername(formData['username'])
        user = list(user)
        if len(user) != 0:
            if user[0]['password'] == hashed_password.hexdigest():
                session['user'] = formData['username']
                return redirect("/index")
            else:
                flash("Invalid password!")
                return render_template('login.html')
        else:
            flash("Invalid username!")
            return render_template('login.html')
    else: 
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        formData = request.form
        username = formData['username']
        email = formData['email']
        password = formData['password']
        hashed_password = hashlib.md5(password.encode())
        mongo = Mongo()

        userDb = mongo.getUsersByUsername(formData['username'])
        if len(list(userDb)) != 0:
            error = "Username already used, please choose other username"
            return render_template('register.html', error=error)
        else:
            userDict = {'username': username, 'email': email, 'password': hashed_password.hexdigest()}
            mongo.insertUser(userDict)
            flash("User registration success!")
            return redirect("/index")
    else: 
        return render_template('register.html')

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        if request.method == "POST":
            mongo = Mongo()
            file = request.files['file']
            if file.filename == '':
                flash("No selected file")
                return render_template('index.html')
            if file:
                if allowedFileExtension(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
                    file.save(filepath)
                    filesize = os.stat(filepath).st_size
                    result = ocr(filename)
                    resultDict = {
                        'filename': filename, 
                        'filesize': filesize, 
                        'filepath': filepath,
                        'ocrtimestamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),  
                        'content': result,
                        'uploaded_by': session['user']
                    }
                    mongo.insertOCRResult(resultDict)
                    return render_template('result.html', result=result)
                else:
                    flash("File type not supported")
                    return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        return redirect("/login")

@app.route("/history", methods=["GET"])
def history():
    if 'user' in session:
        mongo = Mongo()
        results = mongo.getByUsername(session['user'])
        resultsList = []

        for result in results:
            resultsList.append(result)
        return render_template('history.html', results=resultsList)
    else:
        return redirect("/login")

@app.route('/open_file', methods=['GET'])
def openFile():
    if 'user' in session:
        args = request.args
        filename = args.get('filename')
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
    else:
        return redirect("/login")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
