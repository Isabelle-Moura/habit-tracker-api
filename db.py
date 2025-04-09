# This is the file that contains all the database logic of the project

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connection with MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))

# Select database
db = client["habit_tracker"]

# Collections (is the same as tables in relational-databases) 
habits_collection = db["habits"]
users_collection = db["users"]

# Function to test connection
def test_connection():
    try:
        client.server_info()  
        print("Conection with MongoDB stablished!")
    except Exception as e:
        print(f"Error while trying to connect with MongoDB: {e}")

if __name__ == "__main__":
    test_connection()