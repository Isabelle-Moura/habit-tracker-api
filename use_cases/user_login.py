# Here's the code to login a user.

from db import users_collection
import bcrypt
import jwt
import datetime

SECRET_KEY = "segredin"  # Substitua por uma chave secreta forte

def login_user(email, password):
    # Buscar o usuário pelo email
    user = users_collection.find_one({"email": email})
    if not user:
        raise ValueError("User not found")

    # Verificar a senha
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise ValueError("Invalid password")

    # Gerar um token JWT
    token = jwt.encode({
        "user_id": str(user["_id"]),
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expira em 24 horas
    }, SECRET_KEY, algorithm="HS256")

    return token