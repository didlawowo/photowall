import glob
import os

from PIL import Image
from flask import Flask, render_template

WALL_FOLDER = os.path.join('static', 'photo')
BRUT_FOLDER = 'brut'


app = Flask(__name__)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

@app.route('/')
@app.route('/index')
def show_index():

    listb = glob.glob1(BRUT_FOLDER,'*.jpg')
    listf = glob.glob1(WALL_FOLDER, '*.jpg')

    listt = diff(listb, listf)
    print(f"found {len(listt)} photo to resize")
    print(f"liste to resize: {listt}")

    for img in listt:
        print(f"resizing {img}")
        image = Image.open(os.path.join('brut', img))
        size=(400,400)
        image.thumbnail(size)
        path_save= ('static/photo')
        image.save(os.path.join(path_save, img))



    listw = sorted(glob.glob(os.path.join(WALL_FOLDER, '*.jpg')))

    return render_template("index.html", images=listw)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)