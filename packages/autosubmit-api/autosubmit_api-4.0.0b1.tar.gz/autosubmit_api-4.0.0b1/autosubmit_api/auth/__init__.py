from functools import wraps
from flask import request
import jwt
from autosubmit_api.config import JWT_ALGORITHM, JWT_SECRET


def with_auth_token(func):
    @wraps(func)
    def inner_wrapper(*args, **kwargs):  
        current_token = request.headers.get("Authorization")
        
        try:
            jwt_token = jwt.decode(current_token, JWT_SECRET, JWT_ALGORITHM)
        except Exception as exp:
            jwt_token = {"user_id": None}

        kwargs["user_id"] = jwt_token.get("user_id", None)

        func(*args, **kwargs)   
            
    return inner_wrapper  