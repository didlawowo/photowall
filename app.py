import glob
import os
from pathlib import Path
from flask_compress import Compress

from PIL import Image
from flask import Flask, flash, request, redirect, render_template,  jsonify
from loguru import logger
from werkzeug.utils import secure_filename


def _clear_history():
    logger.info('Drop old images in photowall')
    files = glob.glob1(WALL_FOLDER, '*.jpg')
    logger.debug(files)
    for f in files:
        # logger.debug(f)
        os.unlink(os.path.join(WALL_FOLDER, f))
    logger.success('Photo Wall dir cleared')


def _diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def _make_picture(client_folder):
    listf = glob.glob1(client_folder, "*.jpg")
    listw = glob.glob1(WALL_FOLDER, '*.jpg')

    listt = _diff(listf, listw)
    logger.info(f"Found {len(listt)} from {client_folder} to resize")
    logger.info(f"list to resize: {listt}")

    for img in listt:
        logger.info(f"Resizing {img}")
        _resize_picture(client_folder, img)

    return listw


def _resize_picture(original_folder, img):
    logger.info('Starting resize all image')
    try:
        image = Image.open(os.path.join(original_folder, img))
        size = (1500, 800)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(os.path.join(WALL_FOLDER, img, ), quality=90, optimize=True)
        logger.success(f'Image {img} saved')
    except Exception as e:
        logger.error(e)


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


### RUN CODE

static = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'jpeg', 'gif'}

app = Flask(__name__, static_folder=static, template_folder='templates')

logger.info(f"{os.environ.get('FLASK_ENV')} mode detected")
event_name = Path(os.environ.get('EVENT'))
dslr_path = Path(os.environ.get('DSLR_PATH'))

WALL_FOLDER = os.path.abspath('static/photowall')
UPLOAD_FOLDER = os.path.abspath('static/upload')
LOGO_FOLDER = os.path.abspath('static/logo_client')
EVENT_FOLDER = Path(dslr_path / event_name / "Singles")

_clear_history()

if os.getenv('FLASK_ENV') == 'development':
    logo_client = os.path.abspath("static/logo/gumpy_transparent.png")
else:
    logo_client = os.path.abspath("static/logo/client.jpg")
    if not os.path.exists(logo_client):
        logger.warning(f'client logo not exist, set gumpy jpg')
        logo_client = os.path.abspath("static/logo/gumpy_transparent.png")

    else:
        logger.success(f'Custom logo client found {logo_client}')

try:
    logger.info('Checking all dirs')
    if not os.path.exists(WALL_FOLDER):
        os.makedirs(WALL_FOLDER)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(LOGO_FOLDER):
        os.makedirs(LOGO_FOLDER)

    if not os.path.exists(EVENT_FOLDER):
        logger.critical(f'Event folder not exist, exit program : {EVENT_FOLDER}')
        exit(1)
    logger.success('All dirs are presents')

except Exception as e:
    logger.error(e)

logger.info(f'Event folder: {EVENT_FOLDER}')


@app.route('/')
@app.route('/index')
def show_index():
    _make_picture(EVENT_FOLDER)
    list_image_photowall = glob.glob1(WALL_FOLDER, '*.jpg')
    logger.info(f'Found {len(list_image_photowall)} pictures in photowall, builoding')

    return render_template("index.html", images=list_image_photowall, logo_client=logo_client)


@app.route('/admin')
def show_admin():
    listw = glob.glob1(WALL_FOLDER, '*.jpg')
    return render_template("admin.html", images=listw)


@app.route('/config/<name>', methods=['GET'])
def set_event_name(name):
    Path(dslr_path / Path(name) / "Singles")
    _make_picture(Path(dslr_path / Path(name) / "Singles"))
    return jsonify({"message": "event configured"})


@app.route('/upload', methods=['POST'])
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
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # return redirect(url_for('upload_file', filename=filename))
            logger.info(f'file {filename} correctly upload to {UPLOAD_FOLDER}')
            _resize_picture(UPLOAD_FOLDER, filename)
            return redirect("/")

    return render_template("upload.html")


@app.route('/delete/<img>')
def delete_pic(img):
    img = img.split('/')[-1]
    logger.info(f"delete img {img}")
    try:
        os.unlink(os.path.join(UPLOAD_FOLDER, img))
    except Exception as e:
        logger.error(e)

    try:
        os.unlink(os.path.join(EVENT_FOLDER, img))
    except Exception as e:
        logger.error(e)

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
    from dotenv import load_dotenv

    load_dotenv()
    _clear_history()
    app.run(host='0.0.0.0', port=5000, debug=True)
    c = Compress()
    c.init_app(app)
