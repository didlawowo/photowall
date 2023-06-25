import os
import pygame
import time
from PIL import Image, ImageDraw, ImageFont

# Folders with pictures
input_folder_path = '../example-photos'  # change this to your image directory
output_folder_path = './watermarked'  # change this to your output directory

# Watermark text
watermark_text = "Capturez des moments inoubliables !"

# Font size for the watermark text
font_size = 40

# Font file path for macOS
font_file_path = '/Library/Fonts/Arial.ttf'  # replace with the actual font file path on macOS

# Path to the image for the watermark
watermark_image_path = './gumpy_logo.png'  # change this to the path of your image

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (width, height)
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Time per slide in seconds
slide_time = 2

# Flag to track screen touch
screen_touched = False

# List of pictures
picture_list = [filename for filename in os.listdir(input_folder_path) if filename.endswith('.jpg') or filename.endswith('.png')]
picture_count = len(picture_list)
current_index = 0

# Clear the contents of the watermarked folder
for filename in os.listdir(output_folder_path):
    file_path = os.path.join(output_folder_path, filename)
    os.remove(file_path)

# Main loop
while not screen_touched:
    # Get the current picture filename
    filename = picture_list[current_index]

    # Open the image using PIL
    img = Image.open(os.path.join(input_folder_path, filename))
    img_height = 100  # Adjust the height to 100 pixels

    # Resize the image while maintaining aspect ratio
    width, height = img.size
    img_width = int(width * (img_height / height))
    img = img.resize((img_width, img_height))

    # Create a watermark band
    watermark_band = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 128))

    # Load the watermark image
    watermark_image = Image.open(watermark_image_path)

    # Position the watermark image at the beginning of the band
    watermark_band.paste(watermark_image, (0, 0))

    # Position the watermark text after the image
    watermark_font = ImageFont.truetype(font_file_path, font_size)
    draw = ImageDraw.Draw(watermark_band)
    text_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = (watermark_image.width, (img_height - text_height) // 2)

    # Add the watermark text to the band
    draw.text(text_position, watermark_text, font=watermark_font, fill='white')

    # Paste the watermark band on top of the image
    img.paste(watermark_band, (0, 0), mask=watermark_band)

    # Save watermarked images to the output directory
    output_path = os.path.join(output_folder_path, filename)
    img.save(output_path)

    # Convert PIL Image to Pygame Surface and display it
    pygame_img = pygame.image.frombuffer(img.tobytes(), img.size, img.mode)
    pygame_img = pygame.transform.scale(pygame_img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.blit(pygame_img, (0, 0))
    pygame.display.flip()

    # Start timer
    start_time = time.time()

    # Slideshow loop
    while time.time() - start_time < slide_time:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_touched = True
                break

    # Increment the index for the next picture
    current_index = (current_index + 1) % picture_count

pygame.quit
