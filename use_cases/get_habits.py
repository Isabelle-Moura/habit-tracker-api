# Here's the code to get all the habits of a user.

from db import habits_collection
from datetime import datetime, timedelta

def get_habits(user_id):
    habits = habits_collection.find({"user_id": user_id})
    return [habit for habit in habits]

def get_habits_by_category(user_id, category):
    habits = habits_collection.find({"user_id": user_id, "category": category})
    return [habit for habit in habits]

def get_habit_stats(user_id):
    habits = get_habits(user_id)
    stats = {
        "total_habits": len(habits),
        "completion_rate": 0,
        "longest_streak": 0
    }
    
    if not habits:
        return stats

    total_completions = 0
    total_possible = 0
    current_streak = 0
    max_streak = 0

    for habit in habits:
        completed_dates = habit.get("completed_dates", [])
        total_completions += len(completed_dates)
        # Calcula dias possíveis desde a criação do hábito
        created_at = habit.get("created_at", datetime.now())
        days_since_creation = (datetime.now() - created_at).days + 1
        total_possible += days_since_creation if habit["frequency"] == "daily" else days_since_creation // 7

        # Calcula streak
        sorted_dates = sorted(completed_dates)
        for i in range(len(sorted_dates)):
            if i == 0:
                current_streak = 1
            elif (sorted_dates[i] - sorted_dates[i-1]).days == 1:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)

    stats["completion_rate"] = (total_completions / total_possible * 100) if total_possible > 0 else 0
    stats["longest_streak"] = max_streak
    return stats