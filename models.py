from datetime import datetime

class User:
    def __init__(self, username, email, password, created_at=None):
        self.username = username
        self.email = email
        self.password = password  
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            created_at=data.get("created_at")
        )

class Habit:
    def __init__(self, user_id, name, frequency, category="Uncategorized", created_at=None, completed_dates=None):
        self.user_id = user_id  # References the User who created the habit
        self.name = name  # Habit name (ex.: "Drink Water", "Exercise")
        self.frequency = frequency  # Frequency of the habit (ex.: "Daily", "Weekly")
        self.category = category  # Category of the habit (ex.: "Health", "Work")
        self.created_at = created_at or datetime.utcnow()
        self.completed_dates = completed_dates or []  # List of dates when the habit was completed

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "frequency": self.frequency,
            "category": self.category,
            "created_at": self.created_at,
            "completed_dates": self.completed_dates
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            frequency=data.get("frequency"),
            category=data.get("category", "Uncategorized"),  
            created_at=data.get("created_at"),
            completed_dates=data.get("completed_dates")
        )