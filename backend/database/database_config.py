from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settins=get_settings()
database_url = settins.DATABASE_URL

engine = create_async_engine(database_url, echo=True)

# Create session
async_session = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, class_=AsyncSession
)

Base = declarative_base()

database = Database(database_url)
