from enum import Enum

class LogMessage(Enum):
    STARTING_APP = "Iniciando o app.py..."
    FLASK_CORS_CONFIGURED = "Flask e CORS configurados."
    STARTING_SERVER = "Iniciando o servidor Flask..."
    SERVER_STARTED = "Servidor Flask iniciado."