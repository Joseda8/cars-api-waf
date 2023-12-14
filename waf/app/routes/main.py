from flask import Blueprint, jsonify, request
import requests

main_bp = Blueprint("main", __name__)

# Define a generic proxy route
@main_bp.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    # Perform WAF security checks here if needed

    # Forward the request to the Node.js service
    node_service_url = f"http://localhost:5000/{path}"
    response = requests.request(
        method=request.method,
        url=node_service_url,
        headers=request.headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Return the Node.js service response to the client
    return response.text, response.status_code, {"Content-Type": "application/json"}


@main_bp.route("/")
def hello_world():
    return jsonify(message="Hello, World!")

@main_bp.route("/about")
def about():
    return jsonify(message="This is the about page.")

@main_bp.route("/contact")
def contact():
    return jsonify(message="You can contact us at contact@example.com.")
