import glob
import os

import qrcode as qrcode
from PIL import Image
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

WALL_FOLDER = "static/photo"
BRUT_FOLDER = 'brut'
UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


@app.route('/')
@app.route('/index')
def show_index():
    listb = glob.glob1(BRUT_FOLDER, '*.jpg')
    listf = glob.glob1(WALL_FOLDER, '*.jpg')

    listt = diff(listb, listf)
    print(f"found {len(listt)} photo to resize")
    print(f"liste to resize: {listt}")

    for img in listt:
        print(f"resizing {img}")
        image = Image.open(os.path.join('brut', img))
        size = (400, 400)
        image.thumbnail(size)
        path_save = ('static/photo')
        image.save(os.path.join(path_save, img))

    listw = sorted(glob.glob(os.path.join(WALL_FOLDER, '*.jpg')))

    return render_template("index.html", images=listw)


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_file', filename=filename))
            return 'file correctly upload'

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/qrcode')
def gen_qrcode():
    qr = qrcode.QRCode(
        version=12,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=8
    )
    qr.add_data('http://localhost')
    qr.make()
    img = qr.make_image(fill_color="black", back_color="#23dda0")
    img.save('static/qrcode/qrcode_test2_2.png')
    return 'ok'

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
