from db import users_collection
import jwt
import os
from datetime import datetime, timedelta
from models import User
import bcrypt
from enums.error_messages import ErrorMessage
from enums.success_messages import SuccessMessage
from utils.response_builder import build_response

SECRET_KEY = os.getenv("SECRET_KEY")

def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if not user:
        return build_response(
            message=ErrorMessage.INVALID_CREDENTIALS.value,
            status="error"
        )

    stored_password = user["password"].encode('utf-8')
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password):
        return build_response(
            message=ErrorMessage.INVALID_CREDENTIALS.value,
            status="error"
        )

    user_obj = User.from_dict(user)

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "email": user_obj.email,
            "exp": datetime.utcnow() + timedelta(hours=24) 
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return build_response(
        message=SuccessMessage.LOGIN_SUCCESSFUL.value,
        status="success",
        data={"token": token}
    )