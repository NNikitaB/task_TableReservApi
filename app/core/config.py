import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv('.ENV'))


class Settings:
    """
    Configuration settings for the application, managing environment-specific database and mode parameters.

    Attributes:
        MODE: Operational mode of the application (default: 'DEV')
        DB: Database connection type (default: 'postgresql+asyncpg')
        DB_HOST: Database host address (default: '127.0.0.1')
        DB_PORT: Database connection port (default: 5432)
        DB_USER: Database user credentials (default: 'user')
        DB_PASS: Database user password (default: 'password')
        DB_NAME: Name of the database (default: 'dbname')
        DB_URL: Constructed database connection URL
        BD_URL_TEST: Test database connection URL (SQLite)
        BD_NAME_TEST: Test database filename
    """

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

