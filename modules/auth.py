# modules/auth.py
from config import ACCESS_TOKEN, IG_USER_ID

def get_access_token():
    # Currently, we are using a static token.
    # Extend this function if you need dynamic token refreshing.
    return ACCESS_TOKEN

def get_instagram_user_id():
    return IG_USER_ID
