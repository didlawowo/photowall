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
font = ImageFont.load_default()


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

        # Create a watermark band
        watermark_band = Image.new('RGBA', (img.width, 100), (0, 0, 0, 128))

        # Position the watermark text in the center of the band
        watermark_font = ImageFont.truetype('arial.ttf', font_size)
        text_width, text_height = draw.textsize(watermark_text, font=watermark_font)
        text_position = ((img.width - text_width) // 2, (100 - text_height) // 2)

        # Add the watermark text to the band
        watermark_draw = ImageDraw.Draw(watermark_band)
        watermark_draw.text(text_position, watermark_text, font=watermark_font, fill='white')

        # Paste the watermark band on top of the image
        img.paste(watermark_band, (0, img.height - 100), mask=watermark_band)

        # Save watermarked images to a new folder
        os.makedirs(output_folder_path, exist_ok=True)
        img.save(os.path.join(output_folder_path, filename))

        # Convert PIL Image to Pygame Surface and display it
        pygame_img = pygame.image.load(os.path.join(output_folder_path, filename))
        pygame_img = pygame.transform.scale(pygame_img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        screen.blit(pygame_img, (0,0))
        pygame.display.flip()
        time.sleep(slide_time)
