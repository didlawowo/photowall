import glob
from PIL import Image
from flask import Flask, render_template
import os

WALL_FOLDER = os.path.join('static', 'photo')
BRUT_FOLDER = 'brut'


app = Flask(__name__)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

@app.route('/')
@app.route('/index')
def show_index():

# todo drop path in list
    listb = glob.glob(os.path.join(BRUT_FOLDER,'*.jpg'))
    listf = glob.glob(os.path.join(WALL_FOLDER, '*.jpg'))
    print(len(listb))
    print(len(listf))

    listt = diff(listb, listf)
    print(listt)
    print(len(listt))
    for img in listt:
        print(f"resize {img}")
        image = Image.open(img)
        size=(600,600)
        image.thumbnail(size)
        path_save= img.replace('brut','static/photo')
        image.save(path_save)

    listf = glob.glob(os.path.join(WALL_FOLDER,'*.jpg'))


    return render_template("index.html", images=listf)

@app.route('/render')
def render():
    listb = glob.glob(os.path.join(BRUT_FOLDER,'*.jpg'))
    print(listb)

    for img in listb:
        print(img)
        image = Image.open(img)
        size=(600,600)
        image.thumbnail(size)
        path_save= img.replace('brut','static/photo')
        image.save(path_save)
    return 'render ok'