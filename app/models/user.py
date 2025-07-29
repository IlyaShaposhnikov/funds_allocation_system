from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя системы.

    Наследует функциональность от:
    - SQLAlchemyBaseUserTable: базовая модель пользователя FastAPI Users
    - Base: базовый класс моделей SQLAlchemy проекта
    """
