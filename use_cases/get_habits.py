from db import habits_collection
from models import Habit
from utils.response_builder import build_response
from enum.success_messages import SuccessMessages

def get_habits(user_id, page=1, limit=10):
    skip = (page - 1) * limit
    habits = habits_collection.find({"user_id": user_id}).skip(skip).limit(limit)
    habits_list = [Habit.from_dict(habit) for habit in habits]
    total_count = habits_collection.count_documents({"user_id": user_id})
    
    return build_response(
        message=SuccessMessages.GET_HABITS.value,
        status="success",
        data=habits_list,
        page=page,
        limit=limit,
        count=total_count
    )

def get_habits_by_category(user_id, category, page=1, limit=10):
    skip = (page - 1) * limit
    habits = habits_collection.find({"user_id": user_id, "category": category}).skip(skip).limit(limit)
    habits_list = [Habit.from_dict(habit) for habit in habits]
    total_count = habits_collection.count_documents({"user_id": user_id, "category": category})
    
    return build_response(
        message=f"{SuccessMessage.GET_HABITS_BY_CATEGORY.value} {category}",
        status="success",
        data=habits_list,
        page=page,
        limit=limit,
        count=total_count
    )