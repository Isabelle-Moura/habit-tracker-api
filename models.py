# This is the models file of the project

from datetime import datetime

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # Em um projeto real, use hash para senhas!
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }

class Habit:
    def __init__(self, user_id, name, frequency, created_at=None, completed_dates=None):
        self.user_id = user_id  # Referência ao ID do usuário
        self.name = name  # Nome do hábito (ex.: "Beber água")
        self.frequency = frequency  # Frequência (ex.: "daily", "weekly")
        self.created_at = created_at or datetime.utcnow()
        self.completed_dates = completed_dates or []  # Lista de datas em que o hábito foi marcado como concluído

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "frequency": self.frequency,
            "created_at": self.created_at,
            "completed_dates": self.completed_dates
        }