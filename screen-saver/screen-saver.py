import os
import pygame
import time
from PIL import Image, ImageDraw, ImageFont

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
slide_time = 2

# Flag to track mouse movement
mouse_moved = False

# Clear the contents of the watermarked folder
for filename in os.listdir(output_folder_path):
    file_path = os.path.join(output_folder_path, filename)
    os.remove(file_path)

# Get the list of picture files
picture_list = [filename for filename in os.listdir(input_folder_path) if filename.endswith('.jpg') or filename.endswith('.png')]
picture_count = len(picture_list)
current_index = 0

# Main loop
while not mouse_moved:
    # Get the current picture filename
    filename = picture_list[current_index]

    # Open the image using PIL
    img = Image.open(os.path.join(input_folder_path, filename))
    draw = ImageDraw.Draw(img)

    # Create a watermark band
    watermark_band = Image.new('RGBA', (100, 100), (0, 0, 0, 128))

    # Load the watermark image
    watermark_image = Image.open(watermark_image_path)

    # Resize the watermark image to fit the band
    watermark_image = watermark_image.resize((100, 100))

    # Position the watermark image in the bottom right corner
    watermark_position = (img.width - 100, img.height - 100)

    # Add the watermark image to the image
    img.paste(watermark_image, watermark_position, mask=watermark_image)

    # Position the watermark text above the image
    watermark_font = ImageFont.truetype(font_file_path, font_size)
    text_width, text_height = draw.textsize(watermark_text, font=watermark_font)
    text_position = (img.width - text_width, img.height - 150)

    # Add the watermark text to the image
    draw.text(text_position, watermark_text, font=watermark_font, fill='white')

    # Save watermarked images to a new folder
    os.makedirs(output_folder_path, exist_ok=True)
    output_path = os.path.join(output_folder_path, filename)
    img.save(output_path)

    # Convert PIL Image to Pygame Surface and display it
    pygame_img = pygame.image.load(output_path)
    pygame_img = pygame.transform.scale(pygame_img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.blit(pygame_img, (0, 0))
    pygame.display.flip()

    # Reset mouse moved flag
    mouse_moved = False

    # Start timer
    start_time = time.time()

    # Slideshow loop
    while not mouse_moved and time.time() - start_time < slide_time:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_moved = True
                break

    # Increment the index for the next picture
    current_index = (current_index + 1) % picture_count

pygame.quit()
