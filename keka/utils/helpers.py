def get_auth_headers(token=None):
    """
    Returns headers for authenticated API requests.
    If token is provided, includes Authorization header.
    """
    headers = {
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def get_token_headers():
    """
    Returns headers for auth token generation requests.
    """
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }