from app.validators.base import BaseValidator


class XssValidator(BaseValidator):
    def validate(self) -> bool:
        """
        Implement specific validation logic for Cross-Site Scripting (XSS).

        Returns:
        bool: True if the request passes XSS validation, False otherwise.
        """
        # Access attributes from the parent class
        method = self.method
        headers = self.headers
        data = self.data
        cookies = self.cookies
        query_params = self.query_params

        # Flag to indicate if the request is safe
        green_flag = True

        # Check for potential XSS in headers
        for key, value in headers.items():
            if isinstance(value, str) and '<script>' in value:
                green_flag = False
                break

        # Check for potential XSS in data
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and '<script>' in value:
                    green_flag = False
                    break

        # Check for potential XSS in cookies
        for key, value in cookies.items():
            if isinstance(value, str) and '<script>' in value:
                green_flag = False
                break

        # Check for potential XSS in query parameters
        for key, value in query_params.items():
            if isinstance(value, str) and '<script>' in value:
                green_flag = False
                break

        return green_flag