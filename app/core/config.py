from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'secretsecret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
