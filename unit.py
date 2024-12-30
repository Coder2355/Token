import pytz
import random
import string
from datetime import datetime, timedelta
from shortzy import Shortzy
from info import API, URL

TOKENS = {}
VERIFIED_USERS = {}

# Generate a unique token
async def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))

# Generate a shortened verification link
async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=API, base_site=URL)
    return await shortzy.convert(link)

# Verify if the user token is valid and not expired
async def verify_token(user_id, token):
    if user_id in TOKENS and TOKENS[user_id]["token"] == token:
        if TOKENS[user_id]["expiry"] > datetime.now(pytz.timezone("Asia/Kolkata")):
            return True
    return False

# Save user verification details
async def save_verification(user_id):
    VERIFIED_USERS[user_id] = datetime.now(pytz.timezone("Asia/Kolkata")) + timedelta(days=1)

# Check if a user is verified
async def is_verified(user_id):
    if user_id in VERIFIED_USERS:
        if VERIFIED_USERS[user_id] > datetime.now(pytz.timezone("Asia/Kolkata")):
            return True
    return False￼Enter
