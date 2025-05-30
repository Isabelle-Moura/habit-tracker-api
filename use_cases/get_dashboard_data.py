from db import habits_collection
from models import Habit
from datetime import datetime, timedelta
from utils.response_builder import build_response
from enums.success_messages import SuccessMessage

def get_dashboard_data(user_id):
    habits = habits_collection.find({"user_id": user_id})
    habits_list = [Habit.from_dict(habit) for habit in habits]
    
    if not habits_list:
        return build_response(
            message="No habits found",
            status="success",
            data={
                "pending_habits": [],
                "completion_rate": 0,
                "total_habits": 0,
                "total_completions": 0,
                "longest_streak": 0,
                "best_habit": None,
                "category_performance": {},
                "weekly_progress": [],
                "avg_completion_time": 0,
                "suggested_habit": None,
                "habits": []
            }
        )

    today = datetime.now().date()
    total_habits = len(habits_list)
    total_completions = 0
    pending_habits = []
    longest_streak = 0
    category_counts = {}
    category_completions = {}
    weekly_progress = [0] * 7

    for habit in habits_list:
        completed_dates = [d.date() for d in habit.completed_dates]
        total_completions += len(completed_dates)
        
        is_pending = False
        if habit.frequency == "daily" and today not in completed_dates:
            is_pending = True
        elif habit.frequency == "weekly" and not any(d >= today - timedelta(days=7) for d in completed_dates):
            is_pending = True
        if is_pending:
            pending_habits.append({"name": habit.name, "category": habit.category})

        sorted_dates = sorted(completed_dates)
        current_streak = 0
        max_streak = 0
        for i in range(len(sorted_dates)):
            if i == 0:
                current_streak = 1
            elif (sorted_dates[i] - sorted_dates[i-1]).days == 1:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)
        longest_streak = max(longest_streak, max_streak)

        category = habit.category
        category_counts[category] = category_counts.get(category, 0) + 1
        category_completions[category] = category_completions.get(category, 0) + len(completed_dates)

        for date in completed_dates:
            days_ago = (today - date).days
            if 0 <= days_ago < 7:
                weekly_progress[6 - days_ago] += 1

    total_possible = sum((datetime.now() - h.created_at).days + 1 if h.frequency == "daily" else ((datetime.now() - h.created_at).days + 1) // 7 for h in habits_list)
    completion_rate = (total_completions / total_possible * 100) if total_possible > 0 else 0

    best_habit = None
    best_score = 0
    suggested_habit = None
    worst_score = 100
    for habit in habits_list:
        completions = len(habit.completed_dates)
        days_since_creation = (datetime.now() - habit.created_at).days + 1
        possible = days_since_creation if habit.frequency == "daily" else days_since_creation // 7
        score = (completions / possible * 100) if possible > 0 else 0
        stars = min(5, max(1, int(score / 20)))
        habit.stars = stars
        if score > best_score:
            best_score = score
            best_habit = {"name": habit.name, "stars": stars}
        if score < worst_score:
            worst_score = score
            suggested_habit = habit.name

    category_performance = {
        cat: (category_completions.get(cat, 0) / (category_counts[cat] * total_possible / total_habits) * 100) if cat in category_counts else 0
        for cat in category_counts
    }

    avg_completion_time = total_completions / total_habits if total_habits > 0 else 0

    dashboard_data = {
        "pending_habits": pending_habits,
        "completion_rate": completion_rate,
        "total_habits": total_habits,
        "total_completions": total_completions,
        "longest_streak": longest_streak,
        "best_habit": best_habit,
        "category_performance": category_performance,
        "weekly_progress": weekly_progress,
        "avg_completion_time": avg_completion_time,
        "suggested_habit": suggested_habit,
        "habits": [h.to_dict() for h in habits_list]
    }

    return build_response(
        message=SuccessMessage.GET_DASH_DATA.value,
        status="success",
        data=dashboard_data
    )