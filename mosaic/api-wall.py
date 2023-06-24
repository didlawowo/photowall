from flask import Flask, send_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from flask_cors import CORS, cross_origin
import os
import glob

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Define your directory path
WATCH_DIRECTORY = "examples/"
MOSAIC_PATH = "mosaic.jpg"

# create a handler for watchdog
class DirectoryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.create_mosaic()

    def create_mosaic(self):
        images = []
        for filename in glob.glob(WATCH_DIRECTORY + '/*.jpg'): 
            images.append(Image.open(filename))

        widths, heights = zip(*(i.size for i in images))

        total_width = max(widths)
        max_height = sum(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        y_offset = 0
        for img in images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height

        new_img.save(MOSAIC_PATH)

handler = DirectoryHandler()
handler.create_mosaic()

observer = Observer()
observer.schedule(handler, path=WATCH_DIRECTORY, recursive=False)
observer.start()

@app.route('/mosaic', methods=['GET'])
@cross_origin()
def get_mosaic():
    return send_file(MOSAIC_PATH, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
