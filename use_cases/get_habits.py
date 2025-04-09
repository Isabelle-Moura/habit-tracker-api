# Here's the code to get all the habits of a user.

from db import habits_collection
from datetime import datetime, timedelta

def get_habits(user_id):
    habits = habits_collection.find({"user_id": user_id})
    return [habit for habit in habits]

def get_habits_by_category(user_id, category):
    habits = habits_collection.find({"user_id": user_id, "category": category})
    return [habit for habit in habits]