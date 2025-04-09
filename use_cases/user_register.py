# Here's the code to register a user.

from db import users_collection
from models import User
import bcrypt

def register_user(username, email, password):
    # Verify if user's e-mail is already taken
    if users_collection.find_one({"email": email}):
        raise ValueError("Email already in use")

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = User(username, email, hashed_password.decode("utf-8"))
    result = users_collection.insert_one(user.to_dict())
    return str(result.inserted_id)