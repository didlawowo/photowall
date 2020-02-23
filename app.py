import glob
import logging
import os

import qrcode as qrcode
from PIL import Image
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

WALL_FOLDER = "static/photowall"
DSLR_FOLDER = 'brut'
UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def make_picture():

    listb = glob.glob1(DSLR_FOLDER, '*.jpg')
    listu = glob.glob1(UPLOAD_FOLDER, "*.jpg")
    listf = glob.glob1(WALL_FOLDER, '*.jpg')

    listtw = diff(listb, listf)
    listtu = diff(listu, listf)
    print(f"found {len(listtw)} from brut to resize")
    print(f"liste to resize: {listtw}")
    print(f"found {len(listtu)} from upload to resize")
    print(f"liste to resize: {listtw}")
    for img in listtw:
        print(f"resizing {img}")
        image = Image.open(os.path.join(DSLR_FOLDER, img))
        size = (600, 600)
        image.thumbnail(size)
        path_save = (WALL_FOLDER)
        image.save(os.path.join(path_save, img))

    for img in listtu:
        print(f"resizing {img}")
        image = Image.open(os.path.join(UPLOAD_FOLDER, img))
        size = (600, 600)
        image.thumbnail(size)
        path_save = (WALL_FOLDER)
        image.save(os.path.join(path_save, img))


    return  listf


@app.route('/')
@app.route('/index')
def show_index():
    listw =make_picture()
    return render_template("index.html", images=listw)


@app.route('/admin')
def show_admin():
    listw = make_picture()
    return render_template("admin.html", images=listw)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # return redirect(url_for('upload_file', filename=filename))
            # return 'file correctly upload'
            return redirect("/")

    return render_template("upload.html")

@app.route('/qrcode/<data>')
def gen_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/qrcode/qr_code.png')
    return f'qr_code generate for {data}'


@app.route('/delete/<img>')
def delete_pic(img):
    img = img.split('/')[-1]
    print(f"delete img {img}")
    try:
        os.unlink(os.path.join(UPLOAD_FOLDER, img))
    except Exception as e:
        logging.debug(e)
    try:
        os.unlink(os.path.join(DSLR_FOLDER, img))
    except Exception as e:
        logging.debug(e)


    os.unlink(os.path.join(WALL_FOLDER, img))
    return f'picture {img} deleted '

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
