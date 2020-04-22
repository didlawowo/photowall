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


def make_picture(FROM_FOLDER):

    listf = glob.glob1(FROM_FOLDER, "*.jpg")
    listw = glob.glob1(WALL_FOLDER, '*.jpg')

    listt = diff(listf, listw)
    print(f"found {len(listt)} from {FROM_FOLDER} to resize")
    print(f"liste to resize: {listt}")

    for img in listt:
        print(f"resizing {img}")
        resize_picture(FROM_FOLDER, img)

    return listw


def resize_picture(FROM_FOLDER, img):
    image = Image.open(os.path.join(FROM_FOLDER, img))
    size = (600, 600)
    image.thumbnail(size)
    path_save = (WALL_FOLDER)
    image.save(os.path.join(path_save, img))


@app.route('/')
@app.route('/index')
def show_index():
    make_picture(DSLR_FOLDER)
    listw=glob.glob1(WALL_FOLDER, '*.jpg')
    return render_template("index.html", images=listw)


@app.route('/admin')
def show_admin():
    listw=glob.glob1(WALL_FOLDER, '*.jpg')
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
            logging.info(f'file {filename} correctly upload to {UPLOAD_FOLDER}')
            resize_picture(FROM_FOLDER=UPLOAD_FOLDER, img=filename)
            return redirect("/")

    return render_template("upload.html")



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
    logging.info(f'Picture {img} deleted ')
    return redirect("/admin")


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
    app.run(host='0.0.0.0', port=8080)
