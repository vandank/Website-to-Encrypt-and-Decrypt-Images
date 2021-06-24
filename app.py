from flask import Flask, flash, render_template, request, url_for, redirect
import pickle
import os
from werkzeug.utils import secure_filename
from encrypt import main_encrypt 
from decrypt import main_decrypt


app = Flask(__name__, template_folder='./Templates/')

@app.route("/")
def home():
    return render_template('home.html')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/encrypt", methods=['GET', 'POST'])
def encrypt_img():
    UPLOAD_FOLDER = 'static/uploaded_images(encrypte)/'
    if request.method == 'POST':
        flag = 0

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        key = request.form['key']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        elif len(key)!=16:
            flash('Key should be of 16 digit')


        if file and allowed_file(file.filename) and len(key)==16:
            filename = secure_filename(file.filename)
            filename.replace(' ', '_')
            file.save(os.path.join(app.config['UPLOAD_FOLDER_en'], filename))
            # print('app=',filename)
            filename = main_encrypt(key, filename)
            flag = 1
            # print(filename)
            return render_template("encrypt_page.html", flag = flag, file_name = filename)

    return render_template("encrypt_page.html")


@app.route("/decrypt", methods=['GET', 'POST'])
def decrypt_img():
    UPLOAD_FOLDER = 'static/uploaded_images(decrypte)/'
    if request.method == 'POST':
        flag = 0
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        key = request.form['key']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        elif len(key)!=16:
            flash('Key should be of 16 digit')

        if file and allowed_file(file.filename) and len(key)==16:
            filename = secure_filename(file.filename)
            # filename.replace(' ', '_')
            file.save(os.path.join(app.config['UPLOAD_FOLDER_de'], filename))
            print(filename)
            filename = main_decrypt(key, filename)
            flag = 1
            print(filename)
            return render_template("decrypt_page.html", flag = flag, file_name = filename)
            
    return render_template("decrypt_page.html")



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER_en'] = 'static/uploaded_images(encrypte)/'
    app.config['UPLOAD_FOLDER_de'] = 'static/uploaded_images(decrypte)/'
    app.run(debug=True)