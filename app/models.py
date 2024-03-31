from keys import user_db, paswor_db
import datetime
from sqlalchemy import ForeignKey
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from typing import AsyncGenerator

#from sqlalchemy.orm import AsyncSession

DATABASE_URL = f"postgresql+asyncpg://{user_db}:{paswor_db}@postgres:5432/my_database"
engine = create_async_engine(DATABASE_URL) # Создание асинхронного движка для работы с базой данных
Base = declarative_base() # Создание базового класса для объявления моделей
Column = sqlalchemy.Column


# if has access to base in the future - None
class UsersBase(Base):
    __tablename__ = 'users_db'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=True)
    password = Column(sqlalchemy.String(100), nullable=False)
    email = Column(sqlalchemy.String(100), nullable=True, unique=True)



# Users Telegram - Main
class UsersTelegram(Base):
    __tablename__ = 'users_telegram'
    id = Column(sqlalchemy.BigInteger, primary_key=True, unique=True, nullable=False, index=True)
    name = Column(sqlalchemy.String(50), nullable=True)
    full_name = Column(sqlalchemy.String(50), nullable=True)
    first_name = Column(sqlalchemy.String(50), nullable=True)
    last_name = Column(sqlalchemy.String(50), nullable=True)
    chat_id = Column(sqlalchemy.BigInteger, nullable=True) # если не пользователь, а от лица группы то свой id, если  user то user_id
    is_admin = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # Админ ли
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # За блокирован ли
    is_good = Column(sqlalchemy.Integer, default=3, server_default="3", nullable=False) # Рейтинг, хз зачем, посмотрим, может скидки.. Без запрета null, default не выставиться
    ###
    settings = relationship("Settings", back_populates="userstelegram", uselist=False)
    stat = relationship("Statistics")
    discussion = relationship("Discussion", back_populates="userstelegram", uselist=False)









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