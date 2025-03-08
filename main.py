# main.py
import os
import logging
from modules.instagram_api import publish_single_media, get_content_publishing_limit, check_credentials
from modules.image_processor import create_post_image  # Assume this function creates/edits your image locally

def main():
    # First, you might want to check your credentials (for read endpoints using graph.instagram.com)
    # Note: check_credentials() might be implemented separately for the Basic Display API.
    # For content publishing, we assume that you have a valid Instagram User Access Token.
    # Uncomment below if you have a check_credentials function configured for publishing.
    account_info = check_credentials()
    if not account_info:
        print("Invalid credentials. Please update your config and try again.")
        return

    # Define your dynamic content
    dynamic_text = "Hello, Instagram! This is an automated post."
    caption = "Automated post via Instagram Graph API."
    
    # Create your image locally using a Canva template, etc.
    # output_image_path = "output/edited_image.png"
    # os.makedirs("output", exist_ok=True)
    # try:
    #     # This function should edit the template image and save it in the output folder.
    #     create_post_image(dynamic_text, output_image_path)
    # except Exception as e:
    #     logging.error(f"Error during image processing: {e}")
    #     return

    # IMPORTANT: Your image must be hosted on a public server.
    # For testing, you can manually upload the image and set its URL below.
    edited_image_url = "https://images.pexels.com/photos/1172064/pexels-photo-1172064.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

    # Publish a single media post (e.g., a single image)
    try:
        media_id = publish_single_media(image_url=edited_image_url, caption=caption)
        print(f"Post published successfully. Instagram Media ID: {media_id}")
    except Exception as e:
        print("Error during posting:", e)
    
    # Optionally, check your content publishing limit
    try:
        limit_info = get_content_publishing_limit()
        print("Content Publishing Limit Info:", limit_info)
    except Exception as e:
        logging.error(f"Error checking publishing limit: {e}")

if __name__ == "__main__":
    main()
