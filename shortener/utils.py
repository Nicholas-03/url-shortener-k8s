import re
import requests
import os
from config import BASE_URL, AUTH_SERVICE_PORT

AUTH_BASE_URL = os.environ.get("AUTH_BASE_URL", "http://127.0.0.1:5001")

def is_valid_url(url):
    if not url:
        return False
    url_pattern = re.compile(
        "((http|https)://)" # Group: http:// or https:// (required)
        "(www.)?" # www. optional
        "[a-zA-Z0-9@:%._\\+~#?&//=]" # One character that can be letter, digit, or these special chars
        "{2,256}" # The domain part must be 2-256 characters long
        "\\.[a-z]" # Dot + a single lowercase letter
        "{2,6}" # Must be 2-6 characters long
        "\\b" # Word boundary
        "([-a-zA-Z0-9@:%._\\+~#?&//=]" # Group: start of path characters
        "*)" # Optional path (0 or more characters)
    )
    return bool(url_pattern.match(url))

def validateToken(token_header):
    if not token_header: return None
    token = token_header.split(" ")[1] if " " in token_header else token_header
    
    response = requests.post(
        f'{AUTH_BASE_URL}/validate',
        json = {'token': token}
    )
        
    if response.status_code == 200:
        data = response.json()
        return data.get('username') # Return username from token
    return None