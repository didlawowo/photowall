import os
import pygame
import time
from PIL import Image, ImageDraw, ImageFont
from loguru import logger

# Configure Loguru logger
logger.add("debug.log", rotation="500 MB", level="DEBUG")

# Folders with pictures and for output
input_folder_path = '../example-photos'  # change this to your image directory
output_folder_path = './watermarked'  # change this to your output directory

# Watermark text
watermark_text = "Capturez des moments inoubliables !"

# Font size for the watermark text
font_size = 40

# Path to the image for the watermark
watermark_image_path = './gumpy_logo.png'  # change this to the path of your image

# Initialize Pygame
pygame.init()

font_file_path = '/Library/Fonts/Arial.ttf'  # replace with the actual font file path on macOS

# Set the width and height of the screen (width, height)
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Time per slide in seconds
slide_time = 3

# Flag to track mouse movement
mouse_moved = False

# Clear the contents of the watermarked folder
for filename in os.listdir(output_folder_path):
    file_path = os.path.join(output_folder_path, filename)
    os.remove(file_path)
    logger.debug(f"Removed file: {file_path}")

# Get the list of picture files
picture_list = [filename for filename in os.listdir(input_folder_path) if filename.endswith('.jpg') or filename.endswith('.png')]
logger.debug(f"Picture list: {picture_list}")

# Watermark all pictures
for filename in picture_list:
    # Open the image using PIL
    img = Image.open(os.path.join(input_folder_path, filename))
    draw = ImageDraw.Draw(img)

    # Calculate the size of the watermark image while preserving its aspect ratio
    watermark_image = Image.open(watermark_image_path)
    width_ratio = img.width / watermark_image.width
    watermark_width = int(watermark_image.width * width_ratio)
    watermark_height = int(watermark_image.height * width_ratio)
    logger.debug(f"Watermark size: {watermark_width}x{watermark_height}")

    # Resize the watermark image
    watermark_image = watermark_image.resize((watermark_width, watermark_height))

    # Position the watermark image in the bottom right corner
    watermark_position = (img.width - watermark_width, img.height - watermark_height)
    logger.debug(f"Watermark position: {watermark_position}")

    # Add the watermark image to the image
    img.paste(watermark_image, watermark_position, mask=watermark_image)

    # Position the watermark text above the image
    watermark_font = ImageFont.truetype(font_file_path, font_size)
    text_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    text_position = (img.width - text_bbox[2], img.height - watermark_height - text_bbox[3])
    logger.debug(f"Text position: {text_position}")

    # Add the watermark text to the image
    draw.text(text_position, watermark_text, font=watermark_font, fill='white')

    # Save watermarked images to a new folder
    os.makedirs(output_folder_path, exist_ok=True)
    output_path = os.path.join(output_folder_path, filename)
    img.save(output_path)
    logger.debug(f"Saved watermarked image: {output_path}")

# Main loop
index = 0

# Start slideshow
while not mouse_moved:
    # Get the current picture filename
    filename = picture_list[index]
    logger.debug(f"Displaying image: {filename}")

    # Open the watermarked image using PIL
    img = Image.open(os.path.join(output_folder_path, filename))

    # Convert PIL Image to Pygame Surface and display it
    pygame_img = pygame.image.load(os.path.join(output_folder_path, filename))
    pygame_img = pygame.transform.scale(pygame_img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.blit(pygame_img, (0, 0))
    pygame.display.flip()

    # Start timer
    start_time = time.time()
    logger.debug("Slideshow started")

    while time.time() - start_time < slide_time:
        # Check if mouse movement is detected
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_moved = True
                break

        if mouse_moved:
            break

    logger.debug("Slideshow paused")

    if mouse_moved:
        break

    # Increment the index for the next picture
    index = (index + 1) % len(picture_list)

pygame.quit()
