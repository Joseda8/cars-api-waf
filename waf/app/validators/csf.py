from app.validators.base import BaseValidator
from flask import Flask, request, session, jsonify

class CsfValidator(BaseValidator):
    def validate(self) -> bool:
        """
        Implement specific validation logic for Cross-Site Forgery (CSRF).

        Returns:
        bool: True if the request passes CSRF validation, False otherwise.
        """
        # Access attributes from the parent class
        method = self.method
        headers = self.headers
        data = self.data
        cookies = self.cookies
        query_params = self.query_params

        # Flag to indicate if the request is safe
        green_flag = True
        
        # Checking the Origin/Referer of request to see if it is the expected one
        expected_origin = 'expected_origin'
        origin = request.headers.get('Origin') or request.headers.get('Referer')
        if(expected_origin != origin):
            print("origin: ",origin)
            green_flag = False
        
        # Get the session id from the cookie
        sessionId = cookies.get("session_id")
        # Get the CSRF token from the cookie
        crfToken = cookies.get("csrf_token")
        # Check if the session exists
        if sessionId in session:
            userSession = session[sessionId]
            # Validate CSRF token
            if(userSession["csrf_token"] != crfToken):
                green_flag = False
        else:
            green_flag = False

        return green_flag
