# modules/instagram_api.py
import requests
import json
import logging
from modules.auth import get_access_token, get_instagram_user_id

# Set your API version (adjust as needed, e.g., v22.0)
API_VERSION = "v22.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}/me"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_credentials():
    """
    Check if the Instagram credentials are valid by retrieving basic account info.
    This example uses the Instagram Basic Display API base URL.
    """
    IG_USER_ID = get_instagram_user_id()  # This can be 'me' if using a user access token
    access_token = get_access_token()
    # Using graph.instagram.com instead of graph.facebook.com
    url = f"{BASE_URL}?fields=id,username,account_type&access_token={access_token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        logging.info(f"Credentials are valid. Account info: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Credential check failed: {e}")
        return None

def create_media_container(image_url=None, video_url=None, media_type="IMAGE", is_carousel_item=False):
    """
    Creates a media container for a single image/video post or a carousel item.
    For single image posts, only image_url is needed.
    For videos/reels/stories, pass media_type (VIDEO, REELS, STORIES) and video_url.
    For carousel items, set is_carousel_item=True.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/media"
    
    # Build payload. For single image post, media_type is omitted.
    payload = {
        "access_token": access_token,
        "image_url": image_url
    }
    if caption:
        payload["caption"] = caption
    if media_type:
        # For videos, reels, or stories, you must provide the media_type and video_url accordingly.
        payload["media_type"] = media_type
        if video_url:
            payload["video_url"] = video_url
    if is_carousel_item:
        payload["is_carousel_item"] = "true"
    if children:
        # For carousel container creation: children is a comma-separated list of container IDs.
        payload["children"] = children
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "id" in result:
            container_id = result["id"]
            logging.info(f"Media container created successfully: {container_id}")
            return container_id
        else:
            error_msg = f"Error creating media container: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during media container creation: {e}")
        raise

def publish_media_container(creation_id):
    """
    Publishes a media container (created in the previous step) to Instagram.
    Returns the Instagram Media ID.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/media_publish"
    payload = {
        "access_token": access_token,
        "creation_id": creation_id
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "id" in result:
            media_id = result["id"]
            logging.info(f"Media published successfully: {media_id}")
            return media_id
        else:
            error_msg = f"Error publishing media: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during media publishing: {e}")
        raise

def publish_single_media(image_url, caption=None, media_type=None, video_url=None):
    """
    Publishes a single media post (image, video, reel, or story) by performing:
      1. Create a media container.
      2. Publish the container.
    Returns the final Instagram Media ID.
    """
    try:
        container_id = create_media_container(
            image_url=image_url,
            caption=caption,
            media_type=media_type,
            video_url=video_url
        )
        media_id = publish_media_container(container_id)
        return media_id
    except Exception as e:
        logging.error(f"Error during single media publishing: {e}")
        raise

def get_content_publishing_limit():
    """
    Checks the current publishing rate limit usage for the Instagram professional account.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/content_publishing_limit"
    params = {
        "access_token": access_token
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        logging.info(f"Content publishing limit: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching publishing limit: {e}")
        raise
