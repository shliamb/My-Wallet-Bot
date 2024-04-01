from dotenv import load_dotenv
import os

# Укажите путь к вашему файлу .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# Загрузите переменные окружения
load_dotenv(dotenv_path)
# Получите переменные окружения
user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')

from sqlalchemy import ForeignKey
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from typing import AsyncGenerator
# from keys import user_db, paswor_db


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
    user_name = Column(sqlalchemy.String(50), nullable=True)
    currency = Column(sqlalchemy.String(10), default="RUB", server_default="RUB", nullable=False)
    lang = Column(sqlalchemy.String(50), default="RUS", server_default="RUS", nullable=False)
    show_balance = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # show the balance when changing
    cash = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    card_1 = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    name_card_1 = Column(sqlalchemy.String(50), nullable=True)
    card_2 = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    name_card_2 = Column(sqlalchemy.String(50), nullable=True)
    card_3 = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    name_card_3 = Column(sqlalchemy.String(50), nullable=True)
    is_admin = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False)
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False)
    did_you_donate = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # !)
    ####
    sessions = relationship("Sessions", back_populates="users_sessions", uselist=False)
    task = relationship("Task", back_populates="users_task", uselist=False)

class Sessions(Base):
    __tablename__ = 'sessions'
    id = Column(sqlalchemy.BigInteger, ForeignKey('user_id.id'), primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    category = Column(sqlalchemy.String(50), default="is no category", server_default="is no category", nullable=False)
    flow = Column(sqlalchemy.String(5), default="-", server_default="-", nullable=False) # expense/income
    amount = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False)
    is_cash = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    card_number = Column(sqlalchemy.Integer, primary_key=True)
    name_card = Column(sqlalchemy.String(50), nullable=True)
    ####
    users_sessions = relationship("User", back_populates="sessions")

class Task(Base):
    __tablename__ = 'task'
    id = Column(sqlalchemy.BigInteger, ForeignKey('user_id.id'), primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    date_changes = Column(sqlalchemy.DateTime, nullable=True)
    task = Column(sqlalchemy.String(50), nullable=True)
    is_complite = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    ####
    users_task = relationship("User", back_populates="task")

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