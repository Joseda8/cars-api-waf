import requests
from flask import Blueprint, jsonify, request, Response
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
    # Perform WAF security checks here if needed

    # Instantiate validators
    validators = [
        CsfValidator(request_obj=request),
        FileInclusionValidator(request_obj=request),
        OriginBlackListValidator(request_obj=request),
        SqlInjectionValidator(request_obj=request),
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
        allow_redirects=False,
    )

    # Extract response data
    response_data: str = response.text
    response_code: int = response.status_code
    # Get original Content-Type or default to "text/plain"
    response_content_type: dict = {"Content-Type": request.headers.get("Content-Type", "text/plain")}
    return response_data, response_code, response_content_type