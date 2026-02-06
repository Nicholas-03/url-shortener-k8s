import re

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