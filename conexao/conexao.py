import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o conteúdo do .env

class configuracao:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
