from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from ocr import *
from db import Mongo
import os

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'pdf')
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "alphafst"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = Mongo()


def allowedFileExtension(filename):
    fileExt = filename.split(".")[1].lower()
    if fileExt in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
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
                    'content': result
                }
                mongo.insertOCRResult(resultDict)
                return render_template('result.html', result=result)
            else:
                flash("File type not supported")
                return render_template('index.html')
    else:
        return render_template('index.html')

@app.route("/history", methods=["GET"])
def get():
    results = mongo.get()
    resultsList = []

    for result in results:
        resultsList.append(result)
    return render_template('history.html', results=resultsList)


if __name__ == '__main__':
    app.run(debug=True)
