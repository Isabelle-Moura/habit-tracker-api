from flask import Flask, request, jsonify
from flask_cors import CORS
from use_cases.create_habit import create_habit
from use_cases.get_habits import get_habits
from use_cases.mark_habit_as_completed import mark_habit_as_completed
from use_cases.user_register import register_user
from use_cases.user_login import login_user
import jwt

print("Iniciando o app.py...")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

print("Flask e CORS configurados.")

SECRET_KEY = "segredin"  # Deve ser a mesma chave usada no user_login.py

# Middleware para verificar o token JWT
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            token = token.replace("Bearer ", "")  # Remove o prefixo "Bearer "
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(current_user_id, *args, **kwargs)
    wrapper.__name__ = f.__name__  # Necessário para evitar erros com Flask
    return wrapper

@app.route("/register", methods=["POST"])
def register_endpoint():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        user_id = register_user(username, email, password)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/login", methods=["POST"])
def login_endpoint():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        token = login_user(email, password)
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@app.route("/habits", methods=["POST"])
@token_required
def create_habit_endpoint(current_user_id):
    data = request.get_json()
    name = data.get("name")
    frequency = data.get("frequency")
    
    if not all([name, frequency]):
        return jsonify({"error": "Missing required fields"}), 400
    
    habit_id = create_habit(current_user_id, name, frequency)
    return jsonify({"habit_id": habit_id}), 201

# Novo endpoint para buscar os hábitos do usuário autenticado
@app.route("/habits", methods=["GET"])
@token_required
def get_habits_endpoint(current_user_id):
    habits = get_habits(current_user_id)
    for habit in habits:
        habit["_id"] = str(habit["_id"])
    return jsonify(habits), 200

@app.route("/habits/<habit_id>/complete", methods=["POST"])
@token_required
def mark_habit_as_completed_endpoint(current_user_id, habit_id):
    success = mark_habit_as_completed(habit_id, current_user_id)
    if success:
        return jsonify({"message": "Habit marked as completed"}), 200
    return jsonify({"error": "Habit not found or unauthorized"}), 404

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True)
    print("Servidor Flask iniciado.")