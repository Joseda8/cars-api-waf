from app import create_app
from flask import Flask

app: Flask = create_app()

if __name__ == "__main__":
    """
    Main entry point for the Flask application.

    If this script is executed directly (not imported as a module),
    the Flask app is created and run with debug mode enabled on port 8000.
    """
    app.run(debug=True, port=8000)
