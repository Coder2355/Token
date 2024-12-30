import random
import string
from datetime import datetime, timedelta
import requests
from info import API, URL

VERIFIED_USERS = {}  # Store verified users in memory

async def generate_token():
    """Generate a unique token for the user."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def get_verify_shorted_link(verify_link):
    """Shorten the verification link using the shortener API."""
    response = requests.get(f"{URL}?api={API}&url={verify_link}")
    if response.status_code == 200:
        return response.json().get("shortenedUrl", verify_link)
    return verify_link

async def verify_token(user_id, token):
    """Check if the token is valid and not expired."""
    user_data = VERIFIED_USERS.get(user_id)
    if user_data and user_data["token"] == token:
        if datetime.now() < user_data["expiry"]:
            return True
    return False

async def save_verification(user_id):
    """Save user verification."""
    VERIFIED_USERS[user_id] = {"verified": True}

async def is_verified(user_id):
    """Check if the user is verified."""
    user_data = VERIFIED_USERS.get(user_id)
    return user_data and user_data.get("verified", False)
