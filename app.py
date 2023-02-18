import base64
from numpy import identity
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, flash, request, redirect, url_for, render_template
import os
import identity
import common
from deepface import DeepFace
app = Flask(__name__, template_folder='templates')
CORS(app)

UPLOAD_FOLDER = "./static/uploads/"
# create this path if not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def get_recognition():
    return render_template("index.html")


@app.route("/identityBack")
def get_identity():
    return render_template("index2.html")

@app.route("/identityFront")
def get_identityBack():
    return render_template("index3.html")


@app.route('/face-verify', methods=['POST'])
def faceVerify():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    files = request.files.getlist("file")
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file_names.append(file_path)
            file.save(file_path)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    result=DeepFace.verify(file_names[0],file_names[1])
    
    for file in file_names:
        os.remove(file)
        
    return result 

@app.route('/identity-back', methods=['POST'])
def identityBack():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    files = request.files.getlist("file")
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file_names.append(file_path)
            file.save(file_path)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    result=identity.getIdentityText(file_names[0])
    
    for file in file_names:
        os.remove(file)
        
    return result   

@app.route('/identity-front', methods=['POST'])
def identityFront():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    files = request.files.getlist("file")
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file_names.append(file_path)
            file.save(file_path)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    portire=common.getPortire(file_names[0])
    id_front_image=common.getImage(file_names[0])
    
    for file in file_names:
        os.remove(file)
        
    return {
        "idFrontImage":id_front_image,
        "portire":portire
    } 

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)