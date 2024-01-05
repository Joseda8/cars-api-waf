from app.validators.base import BaseValidator

import csv
import pandas as pd
from flask import request
from flask import Blueprint
main_bp = Blueprint("main", __name__)

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
        df = pd.read_csv(main_bp.root_path+"/black_list_files/list.csv")
        
        if request.remote_addr in (df['ip']).tolist():
            green_flag = False

        return green_flag
