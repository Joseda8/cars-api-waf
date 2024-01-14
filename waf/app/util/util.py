import secrets


def generate_csrf_token():
    """
    Generate a CSRF token.

    Returns:
    str: A randomly generated CSRF token.
    """
    token = secrets.token_hex(16)
    return token
