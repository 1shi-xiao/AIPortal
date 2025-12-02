# Alembic 数据库迁移配置
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置和模型
from app.core.config import settings
from app.db.database import Base
from app.models import *  # 导入所有模型

# 这是Alembic Config对象，它提供
# 访问 .ini 文件中的值
config = context.config

# 解释用于Python日志记录的config文件
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 添加你的模型元数据对象
# 用于 'autogenerate' 支持
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """在'offline'模式下运行迁移。"""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """在'online'模式下运行迁移。"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()