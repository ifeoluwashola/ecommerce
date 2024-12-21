from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from api.v1.database.db import Base
from api.v1.app.admin.models.admin_model import user
from api.v1.app.models.user_model import User
from api.v1.utils.config import settings
from alembic import context

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for Alembic
target_metadata = Base.metadata

# Database URL from settings
def get_url():
    return settings.DATABASE_URL

# Database connection configuration
def run_migrations_offline():
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()