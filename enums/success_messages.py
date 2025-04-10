from enum import Enum

class SuccessMessage(Enum):
    USER_REGISTERED = "User registered successfully"
    HABIT_REGISTERED = "Habit registered successfully"
    HABIT_UPDATED = "Habit updated successfully"
    HABIT_DELETED = "Habit deleted successfully"
    HABIT_COMPLETED = "Habit completed successfully"
    GET_DASH_DATA = "Dashboard data retrieved successfully"
    GET_HABITS = "Habits retrieved successfully" 
    GET_HABITS_BY_CATEGORY = "Habits retrieved successfully in the following category: "