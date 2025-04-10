from db import users_collection
from models import User
import bcrypt
from enums.error_messages import ErrorMessage
from enums.success_messages import SuccessMessage
from utils.response_builder import build_response

def register_user(username, email, password):
    if users_collection.find_one({"email": email}):
        return build_response(
            message=ErrorMessage.EMAIL_ALREADY_REGISTERED.value,
            status="error"
        )

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    user = User(username=username, email=email, password=hashed_password.decode("utf-8"))
    
    result = users_collection.insert_one(user.to_dict())
    user_id = str(result.inserted_id)
    
    return build_response(
        message=SuccessMessage.USER_REGISTERED.value,
        status="success",
        data={"user_id": user_id}
    )