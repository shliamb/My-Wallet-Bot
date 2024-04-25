from keys import user_db, paswor_db
import logging
import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, User, Sessions, Task
from sqlalchemy import select, insert, update, extract, join, func
from datetime import datetime, timezone, timedelta

async def create_async_engine_and_session():                               # localhost @postgres
    engine = create_async_engine(f"postgresql+asyncpg://{user_db}:{paswor_db}@localhost:5432/my_database") # echo=True - вывод логирования
    async_session = sessionmaker(bind=engine, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_session


#### USER PROPERTY #### 
# Read User Data
async def get_user_by_id(id: int):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        # Выполняем запрос на выборку данных пользователя из таблицы User по переданному идентификатору
        query = select(User).filter(User.id == id)
        result = await session.execute(query)
        # Получаем первую строку, которая соответствует запросу
        data = result.scalar_one_or_none()  # - это метод SQLAlchemy, который возвращает ровно один результат из результата запроса или None, если запрос не вернул ни одного результата.
        return data or None

# Update User Data
async def update_user(id: int, updated_data) -> bool: 
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        try:
            query = update(User).where(User.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            logging.info(f"User data is update")
            return True
        except Exception as e:
            logging.error(f"Failed to update user data, error: {e}")
            return False

# Add User Data to DB
async def adding_user(user_data) -> bool:
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        try:
            query = insert(User).values(**user_data)
            await session.execute(query)
            await session.commit()
            logging.info("User data is add")
            return True
        except Exception as e:
            logging.error(f"Failed to add user data, error: {e}")
            return False

# Read ALL Users to ADMIN
async def get_all_users_admin():
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(User)
        result = await session.execute(query)
        data = result.scalars().all()
        return data or None
    

#### USERS SESSION #### 
# Read User Session
async def get_session_by_id(id: int):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Sessions).filter(Sessions.id == id)
        result = await session.execute(query)
        data = result.scalar_one_or_none()
        return data or None

# # Update User Session - скорее всего не нужно
# async def update_session(id: int, updated_session) -> bool: 
#     async_session = await create_async_engine_and_session()
#     confirmation = False
#     async with async_session() as session:
#         try:
#             query = update(Sessions).where(Sessions.id == id).values(**updated_session)
#             await session.execute(query)
#             await session.commit()
#             confirmation = True
#             logging.info(f" update session {id}")
#         except Exception as e:
#             logging.error(f"Failed to update session: {e}")
#     return confirmation

# Add User Session to DB
async def adding_session(session_data) -> bool:
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        try:
            query = insert(Sessions).values(**session_data)
            await session.execute(query)
            await session.commit()
            logging.info("Session is add")
            return True
        except Exception as e:
            logging.error(f"Failed to add session, error: {e}")
            return False

# Get all sessions
async def get_all_session():
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Sessions)
        result = await session.execute(query)
        data = result.scalars().all()
        return data or None


# Get all sessions at ID
async def get_all_session_at_id(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Sessions).filter(Sessions.users_id == id)
        result = await session.execute(query)
        data = result.scalars().all()
        return data or None
# All sessions of one user per month/period


# Получить все сессии по ID пользователя за текущий месяц и год
async def get_session_by_month(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:

        time_correction = +3 # Moscow
        utc_zone = timezone.utc
        a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
        a = a + timedelta(hours=time_correction)
        month = int(a.strftime("%m"))
        year = int(a.strftime("%Y"))

        query = (
        select(Sessions)
        .filter(Sessions.users_id == id) 
        .filter(Sessions.amount != 0) # Не нулевые транзакции
        .filter(Sessions.category != "moving") # Не перемещения
        .filter(
            extract('month', Sessions.date) == month,
            extract('year', Sessions.date) == year
        )
        )
        result = await session.execute(query)
        data = result.scalars().all()
        return data or None





# Maybe any think else

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!...





#### Task #### 
# Read Task
async def get_task_by_id(id: int):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Task).filter(Task.id == id)
        result = await session.execute(query)
        data = result.scalar_one_or_none()
        return data or None

# Update Task
async def update_task(id: int, updated_task_data) -> bool: 
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        try:
            query = update(Task).where(Task.id == id).values(**updated_task_data)
            await session.execute(query)
            await session.commit()
            logging.info(f"Task is update by user: {id}")
            return True
        except Exception as e:
            logging.error(f"Failed to update task, error: {e}")
            return False

# Add Task
async def adding_task(task_data) -> bool:
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        try:
            query = insert(Task).values(**task_data)
            await session.execute(query)
            await session.commit()
            logging.info("Adding one task to DB")
            return True
        except Exception as e:
            logging.error(f"Failed to add task, errror:: {e}")
            return False