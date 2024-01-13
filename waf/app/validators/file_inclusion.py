import os
from app.validators.base import BaseValidator


class FileInclusionValidator(BaseValidator):
    def validate(self) -> bool:
        """
        Implement specific validation logic for File Inclusion Vulnerability.

        Returns:
        bool: True if the request passes file inclusion vulnerability validation, False otherwise.
        """
        # Access attributes from the parent class
        method = self.method
        headers = self.headers
        data = self.data
        cookies = self.cookies
        query_params = self.query_params

        # Flag to indicate if the request is safe
        green_flag = True

        # Validate input for potential file inclusion vulnerability
        if "file" in query_params:
            file_path = query_params["file"]
            # Ensure the file path is a valid, allowed path and does not contain ".."
            if not self.is_valid_file_path(file_path):
                green_flag = False

        return green_flag

    def is_valid_file_path(self, file_path: str) -> bool:
        """
        Validate if the provided file path is valid and safe.

        Args:
        file_path (str): The file path to be validated.

        Returns:
        bool: True if the file path is valid, False otherwise.
        """
        # Define a list of allowed directories or patterns
        allowed_directories = ["/safe_directory/", "/another_safe_directory/"]

        # Define a list of allowed file extensions
        allowed_extensions = [".txt", ".csv", ".html"]

        # Check if the file path is within the allowed directories, does not contain "..", and has an allowed extension
        for allowed_dir in allowed_directories:
            if file_path.startswith(allowed_dir) and ".." not in file_path:
                _, file_extension = os.path.splitext(file_path)
                if file_extension in allowed_extensions:
                    return True

        # If the file path doesn't match any allowed criteria, consider it unsafe
        return False
