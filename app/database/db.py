from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession,AsyncAttrs
from sqlalchemy.orm import DeclarativeBase,declarative_base
from sqlalchemy_utils import database_exists, create_database # type: ignore
from sqlalchemy import MetaData
from app.core import logger
from app.core.config import settings
from app.models.Base import Base


url = ""

if settings.MODE == "TEST":
    url = settings.BD_URL_TEST
    logger.debug("TEST MODE")
else:
    url = settings.DB_URL
    logger.info("PROD MODE")

#logging.basicConfig(level=logging.DEBUG)
#url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
#url = "sqlite+aiosqlite://"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(url=url,pool_size=100,max_overflow=200,)
logger.info(f"Database engine created with URL: {url}")

if settings.MODE == "TEST":
    engine = create_async_engine(url=url)


#if not database_exists(engine.url):
#    create_database(engine.url)


# Создание session maker для асинхронных сессий
async_session_maker = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False,autoflush=False,autocommit=False,)



#class Base(DeclarativeBase):
#    abstract = True
#    pass

#Base = declarative_base()

# generator async session
async def get_async_session():
    #await create_tables()
    async with async_session_maker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        logger.info(" Creating tables in the database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info(" Tables created successfully.")

