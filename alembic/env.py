import sys
import os
import urllib.parse
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Config.config import settings 
from Config.database import Base
from Models.Student import Student 
from Models.Course import Course  
from Models.User import UserModel
from Models.Enrollement import enrollment_association

target_metadata = Base.metadata

config = context.config

password = urllib.parse.quote_plus(settings.DB_PASS)
database_url = f"mysql+pymysql://{settings.DB_USER}:{password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Keep your debug print to verify
print(f"Connecting to: {database_url}")
config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_server_default=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = create_engine(database_url, poolclass=pool.NullPool)

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