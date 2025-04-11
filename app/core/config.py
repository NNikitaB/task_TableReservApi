import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv('.ENV'))


class Settings:
    MODE: str = os.environ.get('MODE', 'DEV')  # Значение по умолчанию
    DB = os.environ.get('DB','postgresql+asyncpg')  # Значение по умолчанию
    DB_HOST: str = os.environ.get('DB_HOST', '127.0.0.1')  # Значение по умолчанию
    DB_PORT: int = int(os.environ.get('DB_PORT', 5432))  # Значение по умолчанию
    DB_USER: str = os.environ.get('DB_USER', 'user')  # Значение по умолчанию
    DB_PASS: str = os.environ.get('DB_PASS', 'password')  # Значение по умолчанию
    DB_NAME: str = os.environ.get('DB_NAME', 'dbname')  # Значение по умолчанию

    DB_URL: str = f'{DB}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    BD_URL_TEST: str = f'sqlite+aiosqlite:///:./testdb.sqlite'
    BD_NAME_TEST:str = "testdb.sqlite"
    
settings = Settings()

