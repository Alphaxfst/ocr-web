from flask import Flask, render_template, request, flash, url_for, session, redirect, send_from_directory, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from ocr import scan
from db import Mongo
import os
import hashlib

parrentDir = os.path.dirname(os.getcwd())

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'pdf')
UPLOAD_DIR = os.path.join(parrentDir, 'OCR_FILES')

app = Flask(__name__)
app.secret_key = "alphafst"


def allowedFileExtension(filename):
    fileExt = filename.split(".")[1].lower()
    return True if fileExt in ALLOWED_EXTENSIONS else False


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
                flash(message="Invalid password!", category="danger")
                return render_template('login.html')
        else:
            flash(message="Invalid username!", category="danger")
            return render_template('login.html')
    else: 
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        mongo = Mongo()

        formData = request.form
        username = formData['username']
        email = formData['email']
        password = formData['password']
        hashed_password = hashlib.md5(password.encode())

        userDb = mongo.getUsersByUsername(formData['username'])
        if len(list(userDb)) != 0:
            flash(message="Username already used, please choose other username", category="danger")
            return render_template('register.html')
        else:
            userDict = {'username': username, 'email': email, 'password': hashed_password.hexdigest()}
            mongo.insertUser(userDict)
            flash(message="User registration success!", category="success")
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
                flash(message="No selected file", category="warning")
                return render_template('index.html')
            if file and allowedFileExtension(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                file.save(filepath)
                filesize = os.stat(filepath).st_size
                result = scan(filename, UPLOAD_DIR)
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
                flash(message="File type not supported", category="danger")
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
        return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)
    else:
        return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
