import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from os.path import abspath, dirname

# 1. Setup paths and load environment variables FIRST
sys.path.insert(0, dirname(dirname(abspath(__file__))))
load_dotenv()

# 2. Grab the URL from the environment
database_url = os.getenv("DATABASE_URL")

# 3. Import models AFTER environment is ready
# This prevents database.py from crashing during the import phase
from models import Base
target_metadata = Base.metadata

# 4. Alembic Config object
config = context.config

# 5. Force Alembic to use the environment variable URL
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Use the configuration that now includes our injected URL
    configuration = config.get_section(config.config_ini_section)
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()