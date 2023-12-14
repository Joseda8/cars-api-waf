from flask import request


class BaseValidator:
    def __init__(self, request_obj: request):
        """
        BaseValidator constructor.

        Parameters:
        - request_obj: The Flask request object to be validated.
        """
        self.request_obj = request_obj
        self.method = request_obj.method
        self.headers = request_obj.headers
        self.data = request_obj.get_data()
        self.cookies = request_obj.cookies

    def validate(self) -> bool:
        """
        Main validation method.
        Override this method in subclasses to implement specific validation logic.

        bool: A boolean indicating whether the request is safe or not.
        """
        raise NotImplementedError("Subclasses must implement the validate method.")
