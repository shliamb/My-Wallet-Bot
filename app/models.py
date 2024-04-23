
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
import sqlalchemy
from typing import AsyncGenerator
import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
user_db, paswor_db = os.environ.get('USER_DB'),  os.environ.get('PASWOR_DB')

#from sqlalchemy.orm import AsyncSession

#DATABASE_URL = f"postgresql+asyncpg://{user_db}:{paswor_db}@postgres:5432/my_database"
DATABASE_URL = f"postgresql+asyncpg://{user_db}:{paswor_db}@localhost:5432/my_database"
engine = create_async_engine(DATABASE_URL) # Создание асинхронного движка для работы с базой данных
Base = declarative_base() # Создание базового класса для объявления моделей
Column = sqlalchemy.Column
####



class User(Base):
    __tablename__ = 'user_id'
    id = Column(sqlalchemy.BigInteger, primary_key=True, unique=True, nullable=False, index=True) # user id telgram or any data id
    name = Column(sqlalchemy.String(1000), nullable=True)
    full_name = Column(sqlalchemy.String(1000), nullable=True)
    first_name = Column(sqlalchemy.String(1000), nullable=True)
    last_name = Column(sqlalchemy.String(1000), nullable=True)
    currency = Column(sqlalchemy.String(100), default="RUB", server_default="RUB", nullable=False)
    lang = Column(sqlalchemy.String(100), default="RUS", server_default="RUS", nullable=False)
    show_balance = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # show the balance when changing
    cash = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    cards = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    money_currency = Column(sqlalchemy.String(10), default="RUB", server_default="RUB", nullable=False)
    crypto = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    crypto_currency = Column(sqlalchemy.String(10), default="USDT", server_default="USDT", nullable=False)
    is_admin = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False)
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False)
    did_you_donate = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # !)
    date = Column(sqlalchemy.DateTime, nullable=True)
    ####
    sessions = relationship("Sessions")


class Sessions(Base):
    __tablename__ = 'sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    category = Column(sqlalchemy.String(1000), default="is no category", server_default="is no category", nullable=False)
    ml_category = Column(sqlalchemy.String(1000), default="is no category", server_default="is no category", nullable=False)
    flow = Column(sqlalchemy.String(50), default="-", server_default="-", nullable=False) # expense/income
    amount = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    is_cash = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    is_cards = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    is_crypto = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    date = Column(sqlalchemy.DateTime, nullable=True)
    ####
    users_id = Column(sqlalchemy.BigInteger, ForeignKey("user_id.id"))

class Task(Base):
    __tablename__ = 'task'
    id = Column(sqlalchemy.BigInteger, ForeignKey('user_id.id'), primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    date_changes = Column(sqlalchemy.DateTime, nullable=True)
    task = Column(sqlalchemy.String(1000), nullable=True)
    is_complite = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 

####

class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(sqlalchemy.Integer, primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    rate = Column(sqlalchemy.Float(), default=100.0, server_default="100.0", nullable=False)
    currency = Column(sqlalchemy.String(10), default="USDT", server_default="USDT", nullable=False)
    ###

class Backup(Base):
    __tablename__ = 'backup'
    id = Column(sqlalchemy.Integer, primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    date_changes = Column(sqlalchemy.DateTime, nullable=True)
    task = Column(sqlalchemy.String(1000), nullable=True)
    is_complite = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    ####
####




# Build Table to DB
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Creature session interactions to DB
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Функция для получения асинхронной сессии
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session