import requests, secrets
from flask import Blueprint, jsonify, request, Response,make_response, session
from typing import Tuple

from app.validators import (
    CsfValidator,
    FileInclusionValidator,
    OriginBlackListValidator,
    SqlInjectionValidator,
    XssValidator,
)

# URL of the service API
SERVICE_API_URL = "http://localhost:5000"

# Endpoints export variable
main_bp = Blueprint("main", __name__)


def generate_csrf_token():
    token = secrets.token_hex(16)
    return token


@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "username" and password == "password":
        # Generate session ID and CSRF token
        session_id = generate_csrf_token()
        csrf_token = generate_csrf_token()
        session[session_id] = {"user": {"username": username, "password": password}, "csrf_token": csrf_token}
        session["test"] = "Jose Montoya"
        response = make_response(jsonify({"message": "Successful login"}))
        response.set_cookie("session_id", session_id, httponly=True)
        response.set_cookie("csrf_token", csrf_token, httponly=True)
        response.status_code = 200
        return response
    else:
        response_code: int = 401
        return jsonify({"message": "invalid credentials"}), response_code
        

@main_bp.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path: str) -> Tuple[str, int, dict]:
    """
    Generic Proxy Route

    This route forwards requests to a service after performing WAF security checks.

    Parameters:
    - path (str): The path extracted from the URL.

    Returns:
    Tuple[str, int, dict]: A tuple containing the service response text, status code, and content type.
    """
    # Check if the path is "/login"
    if path == "login":
        return jsonify({"error": "Access to /login via proxy is not allowed"}), 403

    # Perform WAF security checks here if needed

    # Instantiate validators
    validators = [
        CsfValidator(request_obj=request),
        FileInclusionValidator(request_obj=request),
        OriginBlackListValidator(request_obj=request),
        # SqlInjectionValidator(request_obj=request),
        XssValidator(request_obj=request),
    ]

    # Check validators
    for validator in validators:
        if not validator.validate():
            # If any validator fails, return an appropriate HTTP error response
            error_message = f"Security validation failed: {validator.__class__.__name__}"
            return jsonify({"error": error_message}), 403

    # Forward the request to the service
    node_service_url = f"{SERVICE_API_URL}/{path}"
    response: Response = requests.request(
        method=request.method,
        url=node_service_url,
        headers=request.headers,
        data=request.get_data(),
        cookies=request.cookies,
        params=request.args,
        allow_redirects=False,
    )

    # Extract response data
    response_data: str = response.text
    response_code: int = response.status_code
    # Get original Content-Type or default to "text/plain"
    response_content_type: dict = {"Content-Type": request.headers.get("Content-Type", "text/plain")}
    return response_data, response_code, response_content_type
