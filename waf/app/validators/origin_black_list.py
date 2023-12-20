from app.validators.base import BaseValidator


class OriginBlackListValidator(BaseValidator):
    def validate(self) -> bool:
        """
        Implement specific validation logic for Origin Blacklist.

        Returns:
        bool: True if the request origin is not in the blacklist, False otherwise.
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

        return green_flag
