# Here's the code to login a user.

from db import users_collection
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def login_user(email, password):
    # Fetch user by e-mail
    user = users_collection.find_one({"email": email})
    if not user:
        raise ValueError("User not found")

    # Verify password
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise ValueError("Invalid password")

    # Generates a JWT Token
    token = jwt.encode({
        "user_id": str(user["_id"]),
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expires in 24 hours
    }, SECRET_KEY, algorithm="HS256")

    return token