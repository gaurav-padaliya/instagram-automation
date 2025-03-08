# modules/instagram_api.py
import requests
import logging
from modules.auth import get_access_token, get_instagram_user_id

# Use the Instagram Graph API base URL for content publishing (v22.0 as per documentation)
BASE_URL = "https://graph.instagram.com/v22.0"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_credentials():
    """
    Check if the Instagram credentials are valid by retrieving basic account info.
    This example uses the Instagram Basic Display API base URL.
    """
    IG_USER_ID = get_instagram_user_id()  # This can be 'me' if using a user access token
    access_token = get_access_token()
    # Using graph.instagram.com instead of graph.facebook.com
    url = f"https://graph.instagram.com/v22.0/me?fields=id,username,account_type&access_token={access_token}"
    
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
    Creates a media container for a single media post.
    
    Parameters:
      image_url (str): Public URL of the image (for IMAGE, STORIES, or as carousel item).
      video_url (str): Public URL of the video (for VIDEO or REELS).
      media_type (str): One of "IMAGE", "VIDEO", "REELS", "STORIES". 
                        For carousels, individual items can be IMAGE or VIDEO.
      is_carousel_item (bool): Set to True if this container is part of a carousel.
    
    Returns:
      str: The Instagram Media Container ID.
    
    Raises:
      Exception: If the API request fails.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    
    payload = {
        "access_token": access_token,
        "media_type": media_type
    }
    
    # For a carousel item, mark it explicitly.
    if is_carousel_item:
        payload["is_carousel_item"] = "true"
    
    # Depending on media type, include the correct URL.
    if media_type in ["IMAGE", "STORIES"]:
        if not image_url:
            raise ValueError("image_url is required for IMAGE or STORIES media type.")
        payload["image_url"] = image_url
    elif media_type in ["VIDEO", "REELS"]:
        if not video_url:
            raise ValueError("video_url is required for VIDEO or REELS media type.")
        payload["video_url"] = video_url
    
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

def create_carousel_container(children, caption=None):
    """
    Creates a carousel container from individual media container IDs.
    
    Parameters:
      children (list): A list of media container IDs (up to 10) for carousel items.
      caption (str): Optional caption for the carousel post.
      
    Returns:
      str: The Instagram Carousel Container ID.
      
    Raises:
      Exception: If the API request fails.
    """
    if not children or not isinstance(children, list):
        raise ValueError("children must be a non-empty list of media container IDs.")
    
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    
    # Join the container IDs as a comma separated string.
    children_str = ",".join(children)
    
    payload = {
        "access_token": access_token,
        "media_type": "CAROUSEL",
        "children": children_str
    }
    if caption:
        payload["caption"] = caption

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "id" in result:
            carousel_container_id = result["id"]
            logging.info(f"Carousel container created successfully: {carousel_container_id}")
            return carousel_container_id
        else:
            error_msg = f"Error creating carousel container: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during carousel container creation: {e}")
        raise

def publish_media_container(creation_id):
    """
    Publishes a media container (single media or carousel) to Instagram.
    
    Parameters:
      creation_id (str): The container ID returned from create_media_container() or create_carousel_container().
    
    Returns:
      str: The published Instagram Media ID.
    
    Raises:
      Exception: If the API request fails.
    """
    IG_USER_ID = get_instagram_user_id()
    access_token = get_access_token()
    url = f"{BASE_URL}/{IG_USER_ID}/media_publish"
    
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
            logging.info(f"Media published successfully. Media ID: {media_id}")
            return media_id
        else:
            error_msg = f"Error publishing media: {result}"
            logging.error(error_msg)
            raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during media publishing: {e}")
        raise

def check_container_status(container_id):
    """
    Checks the publishing status of a media container.
    
    Parameters:
      container_id (str): The Instagram Container ID.
      
    Returns:
      str: The status_code (EXPIRED, ERROR, FINISHED, IN_PROGRESS, or PUBLISHED).
      
    Raises:
      Exception: If the API request fails.
    """
    access_token = get_access_token()
    url = f"{BASE_URL}/{container_id}"
    params = {
        "access_token": access_token,
        "fields": "status_code"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        status_code = result.get("status_code")
        logging.info(f"Container {container_id} status: {status_code}")
        return status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during status check: {e}")
        raise
