from flask import Flask, flash, render_template, request, url_for, redirect
import pickle
import os
from werkzeug.utils import secure_filename
from encrypt import main_encrypt 

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__, template_folder='./Templates/')

@app.route("/")
def home():
    return render_template('home.html')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/encrypt", methods=['GET', 'POST'])
def encrypt_img():
    if request.method == 'POST':
        # print('in if')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        key = request.form['key']
        # print(key)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        elif len(key)!=16:
            flash('Key should be of 16 digit')
        if file and allowed_file(file.filename) and len(key)==16:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main_encrypt(key, file.filename)
            return render_template("home.html")
    return render_template("encrypt_page.html")
    # if request.method == 'POST':
    #     print("in if")
    #     ip_img = request.files['ip_image']
    #     key = request.form['key']
    #     ip_img.save(ip_img.filename)
    #     return render_template("encrypt_page.html")
    # print('not in if')
    # return render_template("encrypt_page.html")


@app.route("/decrypt", methods=['GET', 'POST'])
def decrypt_img():
    print('hello')
    if request.method == 'POST':
        print("in if")
        return render_template("decrypt_page.html")
    print('not in if')
    return render_template("decrypt_page.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)