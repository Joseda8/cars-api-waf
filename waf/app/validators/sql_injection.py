import os
import json
from urllib.parse import unquote
from datetime import datetime

from app.validators.base import BaseValidator

# these are needed for loading dataset and trained model files. 
from flask import Blueprint, request
main_bp = Blueprint("main", __name__)


# ML model 
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

df_raw_text = pd.read_csv(main_bp.root_path+"/ml_files/sql_dataset.csv")

# init vectorizer for tranfomation
vectorizer = CountVectorizer(min_df=2, max_df=0.7, stop_words=stopwords.words('english'))
# transform text to numbers (vectorizing)
vectorizer.fit_transform(df_raw_text['Query'].values.astype('U')).toarray()
# load saved model
loaded_model = joblib.load(main_bp.root_path+"/ml_files/trained_model_with_94_percent_accuracy.sav")

class SqlInjectionValidator(BaseValidator):
    def validate(self) -> bool:
        """
        Implement specific validation logic for SQL injection.

        Returns:
        bool: True if the request does not attempt a SQL injection, False otherwise.
        """
        # Access attributes from the parent class
        method = self.method
        headers = self.headers
        data = self.data
        cookies = self.cookies
        query_params = self.query_params
        url = self.request_obj.url 

        green_flag = True

        if method in ("GET", "DELETE"):
            for string_to_check in unquote(url).split('/'):
                if not ml_model(string_to_check): 
                    green_flag = False
                    break

        elif method in ("POST", "PUT"):
            for key, value in (json.loads(data)[0]).items():
                if type(value) == str:
                    if not ml_model(value): 
                        green_flag = False
                        break

        # add to black list
        if green_flag == False:
            with open(main_bp.root_path+"/black_list_files/list.csv", 'a') as file:
                new_record = str(request.remote_addr) + ", "+ "sql injection" + ", "+ str(datetime.now())
                file.write(new_record + '\n')

        return green_flag


def ml_model(text_must_be_checked):
    # transform text to numbers (vectorizing)
    vectorized_req = vectorizer.transform([text_must_be_checked])

    # prediction
    result = loaded_model.predict(vectorized_req)
    
    if result[0] == 1:
        return False # an injection detected
    
    return True
