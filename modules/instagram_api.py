# modules/instagram_api.py
import requests
import logging
from modules.auth import get_access_token, get_instagram_user_id

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_credentials():
    """
    Check if the Instagram credentials are valid by retrieving account info.
    Returns account info if successful, or None if there's an error.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"https://graph.facebook.com/v16.0/{IG_USER_ID}"
    params = {
        "fields": "id,username,name",
        "access_token": access_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        logging.info(f"Credentials are valid. Account info: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Credential check failed: {e}")
        return None

def create_media_container(image_url, caption):
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    creation_url = f"https://graph.facebook.com/v16.0/{IG_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    
    try:
        response = requests.post(creation_url, data=payload)
        response.raise_for_status()
        result = response.json()
        if "id" in result:
            logging.info(f"Media container created successfully: {result['id']}")
            return result["id"]
        else:
            error_msg = f"Error creating media container: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during media container creation: {e}")
        raise

def publish_media(creation_id):
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    publish_url = f"https://graph.facebook.com/v16.0/{IG_USER_ID}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    
    try:
        response = requests.post(publish_url, data=payload)
        response.raise_for_status()
        result = response.json()
        if "id" in result:
            logging.info(f"Media published successfully: {result['id']}")
            return result["id"]
        else:
            error_msg = f"Error publishing media: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during media publishing: {e}")
        raise

def post_to_instagram(image_url, caption):
    try:
        creation_id = create_media_container(image_url, caption)
        post_id = publish_media(creation_id)
        logging.info(f"Post published successfully. Post ID: {post_id}")
        return post_id
    except Exception as e:
        logging.error(f"Error during posting: {e}")
        raise
