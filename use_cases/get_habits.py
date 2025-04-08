# Here's the code to get all the habits of a user.

from db import habits_collection

def get_habits():
    habits = habits_collection.find()
    return [habit for habit in habits]  # Retorna uma lista de hábitos