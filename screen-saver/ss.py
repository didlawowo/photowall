import os
import pygame
import time
from PIL import Image, ImageDraw, ImageFont

# Folders with pictures and for output
input_folder_path = 'C:/Users/your_username/Pictures'  # change this to your image directory
output_folder_path = 'C:/Users/your_username/Pictures/Watermarked'  # change this to your output directory

# Watermark text
watermark_text = "venez prendre une photo"

# You can specify a .ttf font file path on your system here
# Font size is the second parameter
font = ImageFont.truetype("arial.ttf", 50)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (width, height)
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Time per slide in seconds
slide_time = 5

# Main loop
for filename in os.listdir(input_folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # add or remove file types as needed
        # Open the image using PIL
        img = Image.open(os.path.join(input_folder_path, filename))
        draw = ImageDraw.Draw(img)

        # Position the text at bottom-right, you can customize as you need
        text_position = (img.width - 500, img.height - 100)

        # Add text to image
        draw.text(text_position, watermark_text, font=font, fill="white")

        # Save watermarked images to a new folder
        os.makedirs(output_folder_path, exist_ok=True)
        img.save(os.path.join(output_folder_path, filename))

        # Convert PIL Image to Pygame Surface and display it
        pygame_img = pygame.image.load(os.path.join(output_folder_path, filename))
        pygame_img = pygame.transform.scale(pygame_img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        screen.blit(pygame_img, (0,0))
        pygame.display.flip()
        time.sleep(slide_time)
