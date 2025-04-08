# Here's the code to create a habit.

from db import habits_collection
from models import Habit

def create_habit(user_id, name, frequency):
    habit = Habit(user_id, name, frequency)
    result = habits_collection.insert_one(habit.to_dict())
    return str(result.inserted_id)  # Retorna o ID do hábito criado