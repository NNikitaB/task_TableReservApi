from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool, Connection

from alembic import context

from app.database.db import Base  # Import Base
from app.core.config import settings  # Import settings

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy URL from settings
config.set_main_option("sqlalchemy.url", settings.DB_URL)

# Define the target metadata for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as async_connection:
        # Run migrations using a synchronous connection
        await async_connection.run_sync(do_migrations)

def do_migrations(sync_connection: Connection):
    """Perform migrations in a synchronous context."""
    context.configure(
        connection=sync_connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,  # Use this for SQLite
    )

    with context.begin_transaction():
        context.run_migrations()

def run_async_migrations():
    """Run migrations using asyncio."""
    asyncio.run(run_migrations_online())

# Check if we are running in offline mode or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async_migrations()


