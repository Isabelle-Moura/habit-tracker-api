# Here's the code to create a habit.

from db import habits_collection
from models import Habit
from enums.success_messages import SuccessMessage

def create_habit(user_id, name, frequency, category="Uncategorized"):
    habit = Habit(user_id=user_id, name=name, frequency=frequency, category=category)
    result = habits_collection.insert_one(habit.to_dict())
    habit_id = str(result.inserted_id)
    return build_response(
        message=SuccessMessage.HABIT_REGISTERED.value,
        status="success",
        data={"habit_id": habit_id}
    )