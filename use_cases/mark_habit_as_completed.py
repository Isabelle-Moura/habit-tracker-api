from db import habits_collection
from datetime import datetime
from models import Habit
from utils.response_builder import build_response
from enums.error_messages import ErrorMessage
from enums.success_messages import SuccessMessage

def mark_habit_as_completed(habit_id, user_id):
    habit = habits_collection.find_one({"_id": habit_id, "user_id": user_id})
    if not habit:
        return build_response(
            message=ErrorMessage.HABIT_NOT_FOUND_OR_UNAUTHORIZED.value,
            status="error"
        )
    
    habit_obj = Habit.from_dict(habit)
    habit_obj.completed_dates.append(datetime.utcnow())
    habits_collection.update_one(
        {"_id": habit_id},
        {"$set": {"completed_dates": habit_obj.completed_dates}}
    )
    return build_response(
        message=SuccessMessage.HABIT_COMPLETED.value,
        status="success"
    )