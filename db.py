# This is the file that contains all the database logic of the project

from pymongo import MongoClient

# Conexão com o MongoDB (ajuste a URI se estiver usando MongoDB Atlas)
# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb+srv://Isa_Moura:hamster@isadatabase.jgwrkwu.mongodb.net/?retryWrites=true&w=majority&appName=isadatabase")

# Selecionar o banco de dados
db = client["habit_tracker"]

# Coleções (equivalentes a tabelas em bancos relacionais)
habits_collection = db["habits"]
users_collection = db["users"]

# Função para testar a conexão
def test_connection():
    try:
        client.server_info()  # Tenta acessar informações do servidor
        print("Conexão com MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")

if __name__ == "__main__":
    test_connection()