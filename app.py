from flask import Flask, request, jsonify
from flask_cors import CORS
from use_cases import (
 create_habit,
 get_habits,
 get_habits_by_category,
 mark_habit_as_completed,
 register_user,
 login_user,
 get_dashboard_data
)
import jwt
from dotenv import load_dotenv
import os
from enums.log_messages import LogMessage
from enums.error_messages import ErrorMessage
from enums.success_messages import SuccessMessage

load_dotenv()

print(LogMessage.STARTING_APP.value)

app = Flask(__name__)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
cors_allow_headers = os.getenv("CORS_ALLOW_HEADERS", "Content-Type,Authorization").split(",")
cors_methods = os.getenv("CORS_METHODS", "GET,POST,OPTIONS").split(",")

CORS(app, resources={
 r"/*": {
 "origins": cors_origins,
 "allow_headers": cors_allow_headers,
 "methods": cors_methods
 }
})

print(LogMessage.FLASK_CORS_CONFIGURED.value)

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
 def wrapper(*args, **kwargs):
 token = request.headers.get("Authorization")
 if not token:
 return jsonify({"error": ErrorMessage.TOKEN_MISSING.value}), 401
 
 try:
 token = token.replace("Bearer ", "")
 data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
 current_user_id = data["user_id"]
 except jwt.ExpiredSignatureError:
 return jsonify({"error": ErrorMessage.TOKEN_EXPIRED.value}), 401
 except jwt.InvalidTokenError:
 return jsonify({"error": ErrorMessage.INVALID_TOKEN.value}), 401
 
 return f(current_user_id, *args, **kwargs)
 wrapper.__name__ = f.__name__
 return wrapper

@app.route("/register", methods=["POST"])
def register_endpoint():
 data = request.get_json()
 username = data.get("username")
 email = data.get("email")
 password = data.get("password")
 
 if not all([username, email, password]):
 return jsonify({"error": ErrorMessage.MISSING_FIELDS.value}), 400
 
 response = register_user(username, email, password)
 status_code = 201 if response["status"] == "success" else 400
 return jsonify(response), status_code

@app.route("/login", methods=["POST"])
def login_endpoint():
 data = request.get_json()
 email = data.get("email")
 password = data.get("password")
 
 if not all([email, password]):
 return jsonify({"error": ErrorMessage.MISSING_FIELDS.value}), 400
 
 response = login_user(email, password)
 status_code = 200 if response["status"] == "success" else 401
 return jsonify(response), status_code

@app.route("/habits", methods=["POST"])
@token_required
def create_habit_endpoint(current_user_id):
 data = request.get_json()
 name = data.get("name")
 frequency = data.get("frequency")
 category = data.get("category", "Uncategorized")
 
 if not all([name, frequency]):
 return jsonify({"error": ErrorMessage.MISSING_FIELDS.value}), 400
 
 response = create_habit(current_user_id, name, frequency, category)
 status_code = 201 if response["status"] == "success" else 400
 return jsonify(response), status_code

@app.route("/habits/category/<category>", methods=["GET"])
@token_required
def get_habits_by_category_endpoint(current_user_id, category):
 page = int(request.args.get("page", 1))
 limit = int(request.args.get("limit", 10))
 response = get_habits_by_category(current_user_id, category, page, limit)
 for habit in response["data"]:
 habit["_id"] = str(habit["_id"])
 return jsonify(response), 200

@app.route("/habits", methods=["GET"])
@token_required
def get_habits_endpoint(current_user_id):
 page = int(request.args.get("page", 1))
 limit = int(request.args.get("limit", 10))
 response = get_habits(current_user_id, page, limit)
 for habit in response["data"]:
 habit["_id"] = str(habit["_id"])
 return jsonify(response), 200

@app.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard_data_endpoint(current_user_id):
 response = get_dashboard_data(current_user_id)
 for habit in response["data"]["habits"]:
 habit["_id"] = str(habit["_id"])
 return jsonify(response), 200

@app.route("/habits/<habit_id>/complete", methods=["POST"])
@token_required
def mark_habit_as_completed_endpoint(current_user_id, habit_id):
 response = mark_habit_as_completed(habit_id, current_user_id)
 status_code = 200 if response["status"] == "success" else 404
 return jsonify(response), status_code

if __name__ == "__main__":
 print(LogMessage.STARTING_SERVER.value)
 port = int(os.getenv("FLASK_PORT", 5000))
 app.run(debug=os.getenv("FLASK_ENV") == "development", port=port)
 print(LogMessage.SERVER_STARTED.value)