from db import habits_collection
from datetime import datetime
from bson import ObjectId

def mark_habit_as_completed(habit_id, user_id):
    # Verify if the habit belongs to the user
    habit = habits_collection.find_one({"_id": ObjectId(habit_id), "user_id": user_id})
    if not habit:
        return False
    
    # Adds the current date to the completed_dates array
    result = habits_collection.update_one(
        {"_id": ObjectId(habit_id)},
        {"$push": {"completed_dates": datetime.utcnow()}}
    )
    return result.modified_count > 0