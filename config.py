from functools import lru_cache
import os

class Settings:
    author: str = 'AP'
    app_name: str = 'Medical Web-Site for Registration'

    ALGORITHM = 'HS256'
    SECRET_KEY = 'cdbb360d8d1406870003f88c9dfe67c9405f3188a3e4424379e1e723b1959bd4'
    ACCESS_TOKEN_TIME = 7
    REFRESH_TOKEN_DAYS = 15
    DATABASE_URL = 'postgresql+asyncpg://postgres:1000@localhost:5432/demo'

@lru_cache()
def get_settings():
    return Settings()