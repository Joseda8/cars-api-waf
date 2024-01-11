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

        # TODO: Make your magic here
        
        sessionId = cookies.get("session_id")
        crfToken = cookies.get("csrf_token")
        print(sessionId)
        print(crfToken)
        session['username'] = "test"
        print(session['username'])
        print(session['test'])
        # Check if the session exists
        if sessionId in session:
            print(sessionId)
            userSession = session[sessionId]
            # Validate CSRF token
            if(userSession.csrfToken != crfToken):
                green_flag = False
        else:
            green_flag = False

        return green_flag
