import glob
import os
from pathlib import Path

from PIL import Image
from flask import Flask, flash, request, redirect, render_template, config
from loguru import logger
from werkzeug.utils import secure_filename

static = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'jpeg', 'gif'}

app = Flask(__name__, static_folder=static, template_folder='templates')
cfg = config.Config('')
cfg.from_pyfile(os.path.abspath('app_conf.py'))
logger.debug(cfg)
app.config.update(cfg)

if os.getenv('FLASK_ENV') =='development':
    event_name = Path("example")
    dslr_path = Path(".")
else:
    event_name = Path(app.config['EVENT_NAME'])
    dslr_path = Path(app.config['DSLR_PATH'])


WALL_FOLDER = os.path.abspath('static/photowall')
UPLOAD_FOLDER = os.path.abspath('static/upload')

if not os.path.exists(WALL_FOLDER):
    os.makedirs(WALL_FOLDER)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client_folder = Path(dslr_path / event_name / "Originals")

if not os.path.exists(client_folder):
    logger.critical(f'client folder not exist, exit program : {client_folder}')
    exit(1)

logger.info(f'client folder:{client_folder}')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
logger.debug(app.config)
logo_client = "static/logo_client/logo.jpg"

if not os.path.exists(logo_client):
    logger.critical(f'client logo not exist, exit program : {logo_client}')
    exit(1)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def make_picture(client_folder):
    listf = glob.glob1(client_folder, "*.jpg")
    listw = glob.glob1(WALL_FOLDER, '*.jpg')

    listt = diff(listf, listw)
    logger.info(f"found {len(listt)} from {client_folder} to resize")
    logger.info(f"liste to resize: {listt}")

    for img in listt:
        logger.info(f"Resizing {img}")
        resize_picture(client_folder, img)

    return listw


def resize_picture(FROM_FOLDER, img):
    try:
        image = Image.open(os.path.join(FROM_FOLDER, img))
        size = (600, 600)
        image.thumbnail(size)
        path_save = (WALL_FOLDER)
        image.save(os.path.join(path_save, img))
        logger.success(f'image {img} saveed')
    except Exception as e:
        logger.error(e)


@app.route('/')
@app.route('/index')
def show_index():
    make_picture(client_folder)
    listw = glob.glob1(WALL_FOLDER, '*.jpg')
    return render_template("index.html", images=listw)


@app.route('/admin')
def show_admin():
    listw = glob.glob1(WALL_FOLDER, '*.jpg')
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
            logger.info(f'file {filename} correctly upload to {UPLOAD_FOLDER}')
            resize_picture(FROM_FOLDER=UPLOAD_FOLDER, img=filename)
            return redirect("/")

    return render_template("upload.html")


@app.route('/delete/<img>')
def delete_pic(img):
    img = img.split('/')[-1]
    logger.info(f"delete img {img}")
    try:
        os.unlink(os.path.join(UPLOAD_FOLDER, img))
    except Exception as e:
        logger.debug(e)
    try:
        os.unlink(os.path.join(client_folder, img))
    except Exception as e:
        logger.debug(e)

    os.unlink(os.path.join(WALL_FOLDER, img))
    logger.info(f'Picture {img} deleted ')
    return redirect("/admin")


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
