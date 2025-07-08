import os, sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# allow imports from project root
sys.path.append(os.getcwd())

from adapters.outgoing.persistence.models import Base  # your SQLAlchemy Base

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Set `target_metadata` for auto-detecting models
target_metadata = Base.metadata

# Dynamically set the database URL from the environment
database_url = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", database_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as conn:
        context.configure(connection=conn, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()