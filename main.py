# main.py
from modules.instagram_api import check_credentials, post_to_instagram
from modules.image_processor import create_post_image
import os

def main():
    # First, check your credentials
    account_info = check_credentials()
    if not account_info:
        print("Invalid credentials. Please update your config and try again.")
        return

    # Define dynamic text and caption for the post
    dynamic_text = "Hello, world! This is my automated post."
    caption = "Automated post using a custom Python script!"

    # Create the post image
    output_image_path = "output/edited_image.png"
    # os.makedirs("output", exist_ok=True)
    # image_path = create_post_image(dynamic_text, output_image_path)

    # Replace the following with your actual public URL for the image
    edited_image_url = "https://images.pexels.com/photos/1172064/pexels-photo-1172064.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
    # Post to Instagram
    try:
        post_id = post_to_instagram(edited_image_url, caption)
        print(f"Post published successfully. Post ID: {post_id}")
    except Exception as e:
        print("Error during posting:", e)

if __name__ == "__main__":
    main()
