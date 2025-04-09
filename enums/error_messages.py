from enum import Enum

class ErrorMessage(Enum):
    TOKEN_MISSING = "Token is missing"
    TOKEN_EXPIRED = "Token has expired"
    INVALID_TOKEN = "Invalid token"
    MISSING_FIELDS = "Missing required fields"
    EMAIL_ALREADY_REGISTERED = "Email already registered"
    INVALID_CREDENTIALS = "Invalid email or password"
    HABIT_NOT_FOUND_OR_UNAUTHORIZED = "Habit not found or unauthorized"