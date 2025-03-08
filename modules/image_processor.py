# modules/image_processor.py
from PIL import Image, ImageDraw, ImageFont
from config import TEMPLATE_IMAGE_PATH, FONT_PATH

def create_post_image(dynamic_text, output_path="output/edited_image.png"):
    # Load the Canva template
    image = Image.open(TEMPLATE_IMAGE_PATH)
    draw = ImageDraw.Draw(image)
    
    # Configure the text style and position
    font_size = 50
    font = ImageFont.truetype(FONT_PATH, font_size)
    text_position = (100, 100)  # Example coordinates
    
    # Draw the dynamic text onto the image
    draw.text(text_position, dynamic_text, font=font, fill="black")
    
    # Save the edited image
    image.save(output_path)
    return output_path
