# Here's the code to create a habit.

from db import habits_collection
from models import Habit

def create_habit(user_id, name, frequency, category="Uncategorized"):
    habit = {
        "user_id": user_id,
        "name": name,
        "frequency": frequency,
        "category": category,  
        "completed_dates": [],
        "created_at": datetime.now()
    }
    result = habits_collection.insert_one(habit)
    return str(result.inserted_id)