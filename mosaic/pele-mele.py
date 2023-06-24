import os
import random
from flask import Flask, send_file

app = Flask(__name__)

# Define the folder containing the images
IMAGE_FOLDER = 'examples/'

# Get a list of image files in the folder
image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]

@app.route('/random-image')
def random_image():
    # Randomly select an image file from the list
    image_file = random.choice(image_files)
    # Generate the path to the selected image file
    image_path = os.path.join(IMAGE_FOLDER, image_file)
    # Serve the image file
    return send_file(image_path, mimetype='image/jpeg')  # Adjust the mimetype based on your image format

if __name__ == '__main__':
    app.run()
