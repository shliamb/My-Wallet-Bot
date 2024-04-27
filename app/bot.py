import logging
# При деплое раскоментить
logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
from worker_db import get_user_by_id, adding_user, adding_session, update_user, get_all_users_admin, get_session_by_month, get_session_stat_year
from functions import is_int_or_float, day_utcnow, re_day, re_month, sum_cat, re_year, unformat_date
from exchange import get_exchange
from category import get_category
from backupdb import backup_db
from restore_db import restore_db
from graph import build_graph, build_graph_hor
from keys import telegram_token, is_admin
import sys
import os
import csv
import asyncio
from io import StringIO, BytesIO
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, Router, html
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, 
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
# from WalletPay import AsyncWalletPayAPI
# from WalletPay import WalletPayAPI, WebhookManager
# from WalletPay.types import Event
# import uuid
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.markdown import hbold


dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
#bot = Bot(telegram) #, default=types.DefaultBotProperties(parse_mode="Markdown")) # Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# router = Router()
# router.message.middleware(ChatActionMiddleware())
                                                                                                

# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    return



# PUSH /START
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await typing(message)

    await message.answer(f"RU\nПривет, {html.bold(message.from_user.full_name)}!\n\n\
    👛 Это бот, который помогает вести статистику доходов и расходов из разных источников. Позволяет\
    дотошно анализировать категории расходов и доходов, предоставляя удобный отчет.\n\
    Для какой то части людей - это очень полезно, например для меня.\n\n\
    Бот позволяет вызвать меню набрав текстом:\n\
    - Наберите текст содержащий 'баланс' для вывода баланса,\n\
    - По аналогии можно набрать: статистика, добавить, убрать, переместить, настройки, графики или фразы содержащие части этих слов.")

# 🗑 При желании, вы можете удалить все данные о транзакциях в базе, нажатием одной кнопки. Подробнее - позже.               
# EN\nHi, {html.bold(message.from_user.full_name)}!\n\n\
#     👛 This is a bot that helps to keep statistics on income and expenses from various sources. Allows\
#     meticulously analyze the categories of expenses and income, providing a convenient report.\n\
#     For some part of people, it is very useful, for example, for me.\n\n\
#     🗑 If desired, you can delete all transaction data in the database by pressing one button. More details later.")
        # Preparing user data
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    date = await day_utcnow()
        # Save user data
    get_user = await get_user_by_id(id)
    if get_user is None:
        push_data_user = {
            "id": id,
            "name": name,
            "full_name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "date": date
        }
        await adding_user(push_data_user)
    else:
        print()
        logging.info(f"The user id:{id} is already in the database.")


    # MENU
    bot_commands = [
        BotCommand(command="/add", description="📈 Приход"),
        BotCommand(command="/del", description="📉 Расход"),
        BotCommand(command="/mov", description="💸 Перемещение"), 
        BotCommand(command="/stat", description="📊 Статистика"),
        # BotCommand(command="/set", description="⚙️ Настройки"),
    ]
    await bot.set_my_commands(bot_commands)
    return










# SUB-MENU

class Form(StatesGroup):
        # Add
    add_cash = State() 
    add_cash_text = State() 
    add_cards = State()
    add_cards_text = State()
    add_crypto = State()
    add_crypto_text = State()
        # Dell
    del_cash = State()
    del_cash_text = State()
    del_cards = State()
    del_cards_text = State()
    del_crypto = State()
    del_crypto_text = State()
        # Move 
    mov_cash = State()
    mov_cash_choice = State()
    mov_card = State()
    mov_card_choice = State()
    mov_crypto = State()
    mov_crypto_choice = State()





######## ADD MONEY ########
@dp.message(Command("add"))
async def menu_add(message: types.Message):
        # Data preparation
    id = user_id(message)
    n = await get_user_by_id(id)
    if n:
        cash = n.cash
        crypto = n.crypto
        money_currency = n.money_currency
        crypto_currency = n.crypto_currency
        cards = n.cards

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💵 Наличность ({round(cash, 3)} {money_currency})", callback_data="add_cash")],
            [InlineKeyboardButton(text=f"💳 Банковские карты ({round(cards, 3)} {money_currency})", callback_data="add_cards")],
            [InlineKeyboardButton(text=f"🎫 Крипта ({round(crypto, 3)} {crypto_currency}) ", callback_data="add_crypto")], 
        ]
    )
    await message.answer("📈 Выберите место куда добавляете деньги", reply_markup=keyboard)







# ADD MONEY CASH --- 1
@dp.callback_query(lambda c: c.data == 'add_cash')
async def process_add_cash(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения наличности:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_cash)

# ADD MONEY CASH --- 2
@dp.message(Form.add_cash, F.content_type.in_({'text'}))
async def invoice_add_cash(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к пополнению:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.add_cash_text)

# ADD MONEY CASH --- 3
@dp.message(Form.add_cash_text, F.content_type.in_({'text'}))
async def invoice_add_cash_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "+"
    is_cash = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_cash = data_user.cash + amount
    money_currency = data_user.money_currency
    push_data_user = {
        "cash": round(all_cash, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Добавлено {amount} {money_currency}. в наличность, присвоена категория - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()











# ADD MONEY CARD --- 1
@dp.callback_query(lambda c: c.data == 'add_cards')
async def process_add_cards(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения банковской карты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_cards)

# ADD MONEY CARD --- 2
@dp.message(Form.add_cards, F.content_type.in_({'text'}))
async def invoice_add_cards(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к пополнению:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.add_cards_text)

# ADD MONEY CARD --- 3
@dp.message(Form.add_cards_text, F.content_type.in_({'text'}))
async def invoice_add_cards_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "+"
    is_cards = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_cards = data_user.cards + amount
    money_currency = data_user.money_currency
    push_data_user = {
        "cards": round(all_cards, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Добавлено {amount} {money_currency} на карты, присвоена категория - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()











# ADD MONEY CRYPTO --- 1
@dp.callback_query(lambda c: c.data == 'add_crypto')
async def process_add_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения крипты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_crypto)

# ADD MONEY CRYPTO --- 2
@dp.message(Form.add_crypto, F.content_type.in_({'text'}))
async def invoice_add_crypto(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к пополнению:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.add_crypto_text)

# ADD MONEY CRYPTO --- 3
@dp.message(Form.add_crypto_text, F.content_type.in_({'text'}))
async def invoice_add_crypto_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "+"
    is_crypto = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_crypto = data_user.crypto + amount
    crypto_currency = data_user.crypto_currency
    push_data_user = {
        "crypto": round(all_crypto, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Добавлено {amount} {crypto_currency} в крипту, присвоена категория - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()








######## DEL MONEY ########

@dp.message(Command("del"))
async def menu_del(message: types.Message):
        # Data preparation
    id = user_id(message)
    n = await get_user_by_id(id)
    if n:
        cash = n.cash
        crypto = n.crypto
        money_currency = n.money_currency
        crypto_currency = n.crypto_currency
        cards = n.cards

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💵 Наличность ({round(cash, 3)} {money_currency})", callback_data="del_cash")],
            [InlineKeyboardButton(text=f"💳 Банковские карты ({round(cards, 3)} {money_currency})", callback_data="del_cards")],
            [InlineKeyboardButton(text=f"🎫 Крипта ({round(crypto, 3)} {crypto_currency}) ", callback_data="del_crypto")], # 🪪🧾📰
        ]
    )
    await message.answer("📉 Выберите место расхода", reply_markup=keyboard)









# DEL MONEY CASH --- 1
@dp.callback_query(lambda c: c.data == 'del_cash')
async def process_del_cash(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму расхода наличности:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.del_cash)

# DEL MONEY CASH --- 2
@dp.message(Form.del_cash, F.content_type.in_({'text'}))
async def invoice_del_cash(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к расходу:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.del_cash_text)

# DEL MONEY CASH --- 3
@dp.message(Form.del_cash_text, F.content_type.in_({'text'}))
async def invoice_del_cash_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "-"
    is_cash = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_cash = data_user.cash - amount
    money_currency = data_user.money_currency
    push_data_user = {
        "cash": round(all_cash, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Потрачено {amount} {money_currency}. из наличности, присвоена категория расхода - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()









# DEL MONEY CARD --- 1
@dp.callback_query(lambda c: c.data == 'del_cards')
async def process_del_cards(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму расхода с банковской карты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.del_cards)

# DEL MONEY CARD --- 2
@dp.message(Form.del_cards, F.content_type.in_({'text'}))
async def invoice_del_cards(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к расходу:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.del_cards_text)

# DEL MONEY CARD --- 3
@dp.message(Form.del_cards_text, F.content_type.in_({'text'}))
async def invoice_add_cards_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "-"
    is_cards = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_cards = data_user.cards - amount
    money_currency = data_user.money_currency
    push_data_user = {
        "cards": round(all_cards, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Потрачено {amount} {money_currency} с карты, присвоена категория - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()











# DEL MONEY CRYPTO --- 1
@dp.callback_query(lambda c: c.data == 'del_crypto')
async def process_del_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму снятия с крипты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.del_crypto)

# DEL MONEY CRYPTO --- 2
@dp.message(Form.del_crypto, F.content_type.in_({'text'}))
async def invoice_del_crypto(message: Message, state: FSMContext):
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
    await message.answer("Введите комментарий к расходу:")
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    await state.set_state(Form.del_crypto_text)

# DEL MONEY CRYPTO --- 3
@dp.message(Form.del_crypto_text, F.content_type.in_({'text'}))
async def invoice_del_crypto_text(message: Message, state: FSMContext):
    id = user_id(message)
    text = message.text
    category = await get_category(text)
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')

    flow = "-"
    is_crypto = True
    date = await day_utcnow()

        # Saving a shared account User
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    all_crypto = data_user.crypto - amount
    crypto_currency = data_user.crypto_currency
    push_data_user = {
        "crypto": round(all_crypto, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is True:
        await message.answer(f"Снято {amount} {crypto_currency} с крипты, присвоена категория - '{category}'")
    else:
        await message.answer("Ошибка в сохранения данных в базу.")

        # Save Session
    push_data_session = {
        "ml_category": category,
        "category": text,
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)

    await state.clear()





######### MOVING #############

@dp.message(Command("mov"))
async def menu_mov(message: types.Message):
        # Data preparation
    id = user_id(message)
    n = await get_user_by_id(id)
    if n:
        cash = n.cash
        crypto = n.crypto
        money_currency = n.money_currency
        crypto_currency = n.crypto_currency
        cards = n.cards

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💵 Наличность ({round(cash, 3)} {money_currency})", callback_data="mov_cash")],
            [InlineKeyboardButton(text=f"💳 Банковские карты ({round(cards, 3)} {money_currency})", callback_data="mov_cards")],
            [InlineKeyboardButton(text=f"🎫 Крипта ({round(crypto, 3)} {crypto_currency}) ", callback_data="mov_crypto")], # 🪪🧾📰
        ]
    )
    await message.answer("📉 Откуда будем перемещать деньги:", reply_markup=keyboard)




# MOVING MONEY CASH TO CARD OR TO CRYPTO--- 1
@dp.callback_query(lambda c: c.data == 'mov_cash')
async def process_mov_cash(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму перемещаемую из наличности:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.mov_cash)

# MOVING MONEY CASH --- 2
@dp.message(Form.mov_cash)
async def invoice_mov_cash(message: Message, state: FSMContext):
    id = user_id(message)
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
        # Сheck cash
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    cash = data_user.cash
    if cash < amount:
        await message.answer("Ошибка: У вас нет столько налички, попробуйте сумму меньше")
        return
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 На карту", callback_data="cash_to_card")], 
            [InlineKeyboardButton(text="🎫 В крипту", callback_data="cash_to_crypto")],

        ]
    )
    await bot.send_message(message.chat.id, f"Выберите место куда перемещаем (RUB):", reply_markup=keyboard)
    await state.set_state(Form.mov_cash_choice)


# MOVING MONEY CASH TO CARD --- 3
@dp.callback_query(Form.mov_cash_choice, lambda c: c.data == 'cash_to_card')
async def process_mov_cash_to_card(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)
    new_cash = data_user.cash - amount
    new_cards = data_user.cards + amount
    push_data_user = {
        "cash": round(new_cash, 3),
        "cards": round(new_cards, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_cash = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_cards = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()


# MOVING MONEY CASH TO CRYPTO --- 3
@dp.callback_query(Form.mov_cash_choice, lambda c: c.data == 'cash_to_crypto')
async def process_mov_cash_to_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)

    one_usd = await get_exchange()
    if one_usd is None:
        one_usd = 100
        logging.error(f"Failed get exchange")
    new_cash = data_user.cash - amount
    new_crypto = data_user.crypto + amount / one_usd
    push_data_user = {
        "cash": round(new_cash, 3),
        "crypto": round(new_crypto, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_cash = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_crypto = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount / one_usd, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено. Возможно, вам придется скорректировать приход с учетом комисии и выбранного курса в P2P. Что учтется ввиде расхода.")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()












# MOVING MONEY CARD TO CASH OR TO CRYPTO--- 1
@dp.callback_query(lambda c: c.data == 'mov_cards')
async def process_mov_card(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму перемещаемую с карты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.mov_card)

# MOVING MONEY CARD --- 2
@dp.message(Form.mov_card)
async def invoice_mov_card(message: Message, state: FSMContext):
    id = user_id(message)
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
        # Сheck cash
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    cards = data_user.cards
    if cards < amount:
        await message.answer("Ошибка: У вас нет столько на карте, попробуйте сумму меньше")
        return
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 В наличку", callback_data="card_to_cash")], 
            [InlineKeyboardButton(text="🎫 В крипту", callback_data="card_to_crypto")],

        ]
    )
    await bot.send_message(message.chat.id, f"Выберите место куда перемещаем (RUB):", reply_markup=keyboard)
    await state.set_state(Form.mov_card_choice)


# MOVING MONEY CASH TO CARD --- 3
@dp.callback_query(Form.mov_card_choice, lambda c: c.data == 'card_to_cash')
async def process_mov_card_to_cash(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)
    new_cards = data_user.cards - amount
    new_cash = data_user.cash + amount
    push_data_user = {
        "cash": round(new_cash, 3),
        "cards": round(new_cards, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_cards = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_cash = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()


# MOVING MONEY CASH TO CRYPTO --- 3
@dp.callback_query(Form.mov_card_choice, lambda c: c.data == 'card_to_crypto')
async def process_mov_card_to_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)

    one_usd = await get_exchange()
    if one_usd is None:
        one_usd = 100
        logging.error(f"Failed get exchange")
    new_cards = data_user.cards - amount
    new_crypto = data_user.crypto + amount / one_usd
    push_data_user = {
        "cards": round(new_cards, 3),
        "crypto": round(new_crypto, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_cards = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_crypto = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount / one_usd, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено. Возможно, вам придется скорректировать приход с учетом комисии и выбранного курса в P2P. Что учтется ввиде расхода.")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()















# MOVING MONEY CRYPTO TO CASH OR TO CARDS--- 1
@dp.callback_query(lambda c: c.data == 'mov_crypto')
async def process_mov_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму перемещаемую с крипты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.mov_crypto)

# MOVING MONEY CACRYPTORD --- 2
@dp.message(Form.mov_crypto)
async def invoice_mov_crypto(message: Message, state: FSMContext):
    id = user_id(message)
        # Data preparation
    amount = await is_int_or_float(message.text)
        # Сheck in
    if amount is None:
        await message.answer("Ошибка: Введите сумму цифрами")
        return
        # Сheck cash
    data_user = await get_user_by_id(id)
    if data_user is None:
        await message.answer("Ошибка: Пользователь не найден, начните с /start")
        return
    crypto = data_user.crypto
    if crypto < amount:
        await message.answer("Ошибка: У вас нет столько в крипте, попробуйте сумму меньше")
        return
        # Сохраняем  данные в state
    await state.update_data(amount=amount)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 В наличку", callback_data="crypto_to_cash")], 
            [InlineKeyboardButton(text="💳 На курту", callback_data="crypto_to_cards")],

        ]
    )
    await bot.send_message(message.chat.id, f"Выберите место куда перемещаем (USD):", reply_markup=keyboard)
    await state.set_state(Form.mov_crypto_choice)


# MOVING MONEY CRYPTO TO CASH --- 3
@dp.callback_query(Form.mov_crypto_choice, lambda c: c.data == 'crypto_to_cash')
async def process_mov_crypto_to_cash(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
    one_usd = await get_exchange()
    if one_usd is None:
        one_usd = 100
        logging.error(f"Failed get exchange")
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)
    new_crypto = data_user.crypto - amount
    new_cash = data_user.cash + amount * one_usd
    push_data_user = {
        "cash": round(new_cash, 3),
        "crypto": round(new_crypto, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_crypto = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_cash = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cash": is_cash,
        "amount": round(amount * one_usd, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()


# MOVING MONEY CRYPTO TO CARDS --- 3
@dp.callback_query(Form.mov_crypto_choice, lambda c: c.data == 'crypto_to_cards')
async def process_mov_card_to_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
        # Извлекаем данные из state
    data = await state.get_data()
    amount = data.get('amount')
    data_user = await get_user_by_id(id)

    one_usd = await get_exchange()
    if one_usd is None:
        one_usd = 100
        logging.error(f"Failed get exchange")
    new_crypto = data_user.crypto - amount
    new_cards = data_user.cards + amount * one_usd
    push_data_user = {
        "crypto": round(new_crypto, 3),
        "cards": round(new_cards, 3),
    }
    confirm_user = await update_user(id, push_data_user)
    if confirm_user is False:
        await bot.send_message(callback_query.from_user.id, "Ошибка в сохранения данных в базу.")
        # Save cash
    flow = "-"
    is_crypto = True
    date = await day_utcnow()
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_crypto": is_crypto,
        "amount": round(amount, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Save card
    flow = "+"
    is_cards = True
        # Save Session
    push_data_session = {
        "category": "moving",
        "flow": flow,
        "is_cards": is_cards,
        "amount": round(amount * one_usd, 3),
        "users_id": id,
        "date": date
    }
    await adding_session(push_data_session)
        # Message
    await bot.send_message(callback_query.from_user.id, "Перемещение сохранено. Возможно, вам придется скорректировать приход с учетом комисии и выбранного курса в P2P. Что учтется ввиде расхода.")
    await bot.answer_callback_query(callback_query.id)
    await state.clear()

























######## Statistic ########
@dp.message(Command("stat"))
async def menu_stat(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Фин. статистика за тек. месяц", callback_data="stat_month")],
            [InlineKeyboardButton(text="📊 Категории расходов за тек. месяц", callback_data="stat_cat_month")],
            [InlineKeyboardButton(text="📊 Категории доходов за тек. месяц", callback_data="stat_add_cat_month")],
            [InlineKeyboardButton(text="📊 Фин. статистика за тек. год", callback_data="stat_year")],
            [InlineKeyboardButton(text="📊 Категории доход за тек. год", callback_data="stat_add_year")],
            [InlineKeyboardButton(text="📊 Категории расход за тек. год", callback_data="stat_del_year")],
        ]
    )
    await message.answer("📊 Выберите вариант статистики:", reply_markup=keyboard)





# Фин. Статистика по id пользователя по дням текущего месяца доход
@dp.callback_query(lambda c: c.data == 'stat_month')
async def process_stat_month(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
    data = await get_session_by_month(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом месяце нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return
    # Собираю доходы - расходы одного дня и вывожу в обной колонке результат, в результате график текущего месяца
    x = []
    y = []
    income = expenses = null_day = null_amount = i = 0

    for n in data:
        i += 1
        day = int(await re_day(n.date))  # Преобразование даты в int
            # USDT 
        if i == 1:
            one_usdt = await get_exchange()
        if n.is_crypto is True:
            amount = float(n.amount) * one_usdt
        else:
            amount = float(n.amount)

        if n.flow == '-':  # n.flow может быть '+' или '-'
            amount = -amount
            expenses = expenses + amount
        elif n.flow == '+':
            income = income + amount

        if null_day == 0:
            null_day = day
            # Получение месяца 
            name_month = await re_month(n.date)

        if day == null_day:
            null_amount += amount
        else:
            x.append(null_day)
            y.append(round(null_amount, 2))
            null_day = day
            null_amount = amount

        if i == len(data):
            x.append(day)
            y.append(round(null_amount, 2))

    name_file = f"graph_{id}.png"
    confirm = await build_graph(id, x, y, name_month, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    await bot.send_message(callback_query.from_user.id, f"Статистика за {name_month}:\n\nОбщий доход: {round(income, 2)}\nОбщий расход: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения





# Статистика категорий расходов за месяц текущий по id пользователя
@dp.callback_query(lambda c: c.data == 'stat_cat_month')
async def process_stat_cat_month(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
    data = await get_session_by_month(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом месяце нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return

    # Получаем траты по категориям, если они не ноль
    flow = "-"
    data_q = await sum_cat(flow, data)
    x = data_q[0]
    y = data_q[1]
    name_month = data_q[2]
    name_file = f"graph_{id}_hor.png"
    add_or_del = "расходов"

    confirm = await build_graph_hor(x, y, add_or_del, name_month, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    #await bot.send_message(callback_query.from_user.id, f"Статистика за {name_month}:\n\nОбщий доход: {round(income, 2)}\nОбщий расход: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения





# Статистика категорий доходов за месяц текущий по id пользователя
@dp.callback_query(lambda c: c.data == 'stat_add_cat_month')
async def process_stat_add_cat_month(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
    data = await get_session_by_month(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом месяце нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return

    # Получаем доходы по категориям, если они не ноль
    flow = "+"
    data_q = await sum_cat(flow, data)
    x = data_q[0]
    y = data_q[1]
    name_month = data_q[2]
    name_file = f"graph_{id}_add_hor.png"
    add_or_del = "доходов"

    confirm = await build_graph_hor(x, y, add_or_del, name_month, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    #await bot.send_message(callback_query.from_user.id, f"Статистика за {name_month}:\n\nОбщий доход: {round(income, 2)}\nОбщий расход: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения





# Фин. Статистика по id пользователя по месяцам текущего года доход - расход
@dp.callback_query(lambda c: c.data == 'stat_year')
async def process_stat_year(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
        # Получение данных из базы
    data = await get_session_stat_year(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом году нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return
        # Собираю доходы - расходы одного месяца и вывожу в обной вертикальной колонке результат, в результате график текущего года
    x = []
    y = []
    income = expenses = amount = null_amount = i = 0
    null_month = ""

    for n in data:
        i += 1
            # Получение месяца из числа в название из даных базы
        name_month = await re_month(n.date)
            # USDT
        if i == 1:
            one_usdt = await get_exchange()
        if n.is_crypto is True:
            amount = float(n.amount) * one_usdt
        else:
            amount = float(n.amount)

        if n.flow == '-':  # n.flow может быть '+' или '-'
            amount = -amount
            expenses = expenses + amount
        elif n.flow == '+':
            income = income + amount

        if null_month == "":
            null_month = name_month
            year = await re_year(n.date) # Получаем год

        if name_month == null_month:
            null_amount += amount
        else:
            x.append(null_month)
            y.append(round(null_amount, 2))
            null_month = name_month
            null_amount = amount

        if i == len(data):
            x.append(name_month)
            y.append(round(null_amount, 2))

    name_file = f"graph_{id}_stat_year.png"
    confirm = await build_graph(id, x, y, year, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    await bot.send_message(callback_query.from_user.id, f"Статистика за {year}:\n\nОбщий доход за год: {round(income, 2)}\nОбщий расход за год: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения







# Статистика категорий доходов за год текущий по id пользователя
@dp.callback_query(lambda c: c.data == 'stat_add_year')
async def process_stat_add_year(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
    data = await get_session_stat_year(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом году нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return

    # Получаем доходы по категориям, если они не ноль
    flow = "+"
    data_q = await sum_cat(flow, data)
    x = data_q[0]
    y = data_q[1]
    name_year = data_q[3]
    name_file = f"graph_{id}_add_hor_year.png"
    add_or_del = "доходов"

    confirm = await build_graph_hor(x, y, add_or_del, name_year, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    #await bot.send_message(callback_query.from_user.id, f"Статистика за {name_month}:\n\nОбщий доход: {round(income, 2)}\nОбщий расход: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения






# Статистика категорий расходов за год текущий по id пользователя
@dp.callback_query(lambda c: c.data == 'stat_del_year')
async def process_stat_del_year(callback_query: types.CallbackQuery):
    await bot.send_chat_action(callback_query.from_user.id, action='typing')

    id = callback_query.from_user.id
    data = await get_session_stat_year(id)

    if data is None:
        await bot.send_message(callback_query.from_user.id, "К сожалению, в этом году нет транзакций.")
        await bot.answer_callback_query(callback_query.id)
        return

    # Получаем доходы по категориям, если они не ноль
    flow = "-"
    data_q = await sum_cat(flow, data)
    x = data_q[0]
    y = data_q[1]
    name_year = data_q[3]
    name_file = f"graph_{id}_del_hor_year.png"
    add_or_del = "расходов"

    confirm = await build_graph_hor(x, y, add_or_del, name_year, name_file) # Построение графика

    if confirm is True and os.path.exists(f"./graph/{name_file}") and os.path.getsize(f"./graph/{name_file}") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(f"./graph/{name_file}"))

        # После передачи графика, тут же удаляю его на сервере
    directory_path = "./graph/"
    file_name_to_delete = name_file

        # Поиск файла в папке
    for filename in os.listdir(directory_path):
        if filename == file_name_to_delete:
                # Путь к файлу, который нужно удалить
            file_path = os.path.join(directory_path, filename)
                # Удаление файла
            os.remove(file_path)
            print(f"INFO: Файл {file_path} был удален на сервере.")
            break  # Прерываем цикл после удаления файла
    else:
        print(f"ERROR: Файл {file_name_to_delete} не найден в папке {directory_path}")

    #await bot.send_message(callback_query.from_user.id, f"Статистика за {name_month}:\n\nОбщий доход: {round(income, 2)}\nОбщий расход: {round(expenses, 2)}\nОстаток: {round(income - (expenses * -1), 2)}")
    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.answer() # Подтверждение получения




















######## SETINGS ########
@dp.message(Command("set"))
async def menu_setings(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            # [InlineKeyboardButton(text="Валюта", callback_data="currency")],
            # [InlineKeyboardButton(text="Язык бота", callback_data="lang")],
            [InlineKeyboardButton(text="Обнуление информации", callback_data="zero")],
            # [InlineKeyboardButton(text="Backup", callback_data="backup")],
        ]
    )
    await message.answer("⚙️ Настройки:", reply_markup=keyboard)

# SET --- currency
@dp.callback_query(lambda c: c.data == 'currency')
async def process_currency(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "currency")
    await bot.answer_callback_query(callback_query.id)

# SET --- lang
@dp.callback_query(lambda c: c.data == 'lang')
async def process_lang(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "lang")
    await bot.answer_callback_query(callback_query.id)



#                                                                           #
############################# SUB-MENU ######################################




######## ADMIN ########
@dp.message(Command("admin"))
async def menu_admin(message: types.Message):
    id = user_id(message)
    if int(is_admin) != id:
        await bot.send_message(message.chat.id, "Извините, такой команды нет.")
        return
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Download Statistic", callback_data="user_stat")],
            [InlineKeyboardButton(text="Download log", callback_data="log")],
            [InlineKeyboardButton(text="Download Backup", callback_data="backup")],
            [InlineKeyboardButton(text="*Upload and Restore DB", callback_data="push_db")],
            [InlineKeyboardButton(text="Задонатить на развитие", callback_data="donate")],
        ]
    )
    await message.answer("⚙️ Админка:", reply_markup=keyboard)

# ADMIN --- user_stat
@dp.callback_query(lambda c: c.data == 'user_stat')
async def process_user_stat(callback_query: types.CallbackQuery):
    # id = user_id(callback_query)
    chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id
    data = await get_all_users_admin()

    all_static = []
    number = 0
    all_static.append(["№", "id", "Имя", "Полное имя", "Первое имя", "Второе имя", "Донатил", "Дата регистрации"])
    
    for user in data:
        number += 1
        id = user.id
        name = user.name
        full_name = user.full_name
        first_name = user.first_name
        last_name = user.last_name
        did_you_donate = user.did_you_donate
        date = user.date

        all_static.append([number, id, name, full_name, first_name, last_name, did_you_donate, date]) # added user data

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # csv file to download
    file_name = f"Admin-statistic.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=chat_id, document=buffered_input_file)
        await bot.answer_callback_query(callback_query.id)
    except:
        print(f"Error sending documentb Admin stat")

# ADMIN --- log
@dp.callback_query(lambda c: c.data == 'log')
async def process_user_log(callback_query: types.CallbackQuery):
    if os.path.exists("./log/app.log") and os.path.getsize("./log/app.log") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile("./log/app.log"))
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(callback_query.from_user.id, "Файл app.log пустой или отсуствует.")
        await bot.answer_callback_query(callback_query.id)

# ADMIN --- backup 
@dp.callback_query(lambda c: c.data == 'backup')
async def process_backup(callback_query: types.CallbackQuery):
    confirmation = await backup_db()
    if confirmation is True:
        await bot.send_message(callback_query.from_user.id, "Резервная копия базы данных создана успешно и представленна ниже. Сохранены 3 последние версии в рабочей папке, остальные удалены.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка создания резервной копии базы данных.")

    await asyncio.sleep(0.5)

    data_folder = Path("./backup_db/")

    files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории

    sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)

    for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
        os.remove(file_to_delete)
    logging.info("Remove all file DB, saved 3 latest files.")

    last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
    logging.info("Download last DB file.")

    await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(last_downloaded_file))
    await bot.answer_callback_query(callback_query.id)




#
# Admin Restore DB
#
# Нажимаю кнопку восстановления, прикрепляю свой файл db бинарный в .sql, он загружается в папку download_db.
# Далее скрипт останавливает все запросы и очищает память, выставляется глобальный флаг, который не допускает  
# пользователям взаимодействовать с базой. Тем временем, очищается полностью и даже разметка работающей базы 
# и полностью переписывается с закаченного файла. Он не удаляется из папки, не думаю что их будет много.
#
 
class Restor_db(StatesGroup):
    load_db = State()


# Push button - restore
@dp.callback_query(lambda c: c.data == 'push_db')
async def process_sub_admin_stat_push(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text="Прикрепи и отправь нужную копию базы данных для восстановления.", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Restor_db.load_db) # Next Step
    await bot.answer_callback_query(callback_query.id) # End typing

# Next step - download db and restore
@dp.message(Restor_db.load_db)
async def load_a_base(message: Message, state: FSMContext):
    # global work_in_progress
    # work_in_progress = True # Блокировка обращений к базе данных всех пользователей

    if not isinstance(message.document, types.Document):
        await message.answer("Вы передали не документ.")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['sql']

    if file_extension not in allowed_extensions:
        await message.answer("Вы передали файл не sql расширения.")
        return    


    # Name file
    date_time = await day_utcnow() # Current date and time
    date = await unformat_date(date_time)
    formtime = str(date[0]) + str(date[1])
    file_name = f"uploaded-db-{formtime}.sql"

    # await asyncio.sleep(0.3)

    file_path = f"./download_db/{file_name}"
    await bot.download(message.document, file_path) # То что прикрепили и отправили, скачивается в папку с новым именем

    await bot.session.close()
    await dp.storage.close()

    confirmation = await restore_db(file_path) # Восстановелние базы

    work_in_progress = False # Восстановление возможности обращения пользователей к базе

    if confirmation == True:
        await message.answer("Восстановление базы данных прошло успешно.")
    else:
        await message.answer("При восстановлении базы данных, что то пошло не так.")


    await state.clear()
    #await state.set_state(Restor_db.restor_db) # Переход к следующему шагу









@dp.message()
async def my_handler(message: Message):
    await typing(message)
    #await asyncio.sleep(2)
    if "баланс" in message.text.lower():
            # Data preparation
        id = user_id(message)
        n = await get_user_by_id(id)
        if n:
            cash = n.cash
            crypto = n.crypto
            money_currency = n.money_currency
            crypto_currency = n.crypto_currency
            cards = n.cards

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"💵 Наличность ({round(cash, 3)} {money_currency})", callback_data="add_cash")],
                [InlineKeyboardButton(text=f"💳 Банковские карты ({round(cards, 3)} {money_currency})", callback_data="add_cards")],
                [InlineKeyboardButton(text=f"🎫 Крипта ({round(crypto, 3)} {crypto_currency}) ", callback_data="add_crypto")], 
            ]
        )
        await message.answer("⚖️ Баланс:", reply_markup=keyboard)
            # USDT
        one_usdt = await get_exchange()
        usdt_crypto = crypto * one_usdt
        await bot.send_message(message.from_user.id, f"Всего налом и на счетах: {round(usdt_crypto + cards + cash, 2)} {money_currency}")

    elif "статист" in message.text.lower() or "граф" in message.text.lower():
        await menu_stat(message)

    elif "добав" in message.text.lower():
        await menu_add(message)

    elif "удал" in message.text.lower() or "убрать" in message.text.lower() or "расход" in message.text.lower():
        await menu_del(message)

    elif "переме" in message.text.lower() or "перекин" in message.text.lower():
        await menu_mov(message)

    elif "настро" in message.text.lower() or "установ" in message.text.lower():
        await menu_setings(message)

    elif "адми" in message.text.lower():
        await menu_admin(message)

    else:
        await message.answer("Я просто бот, напишите понятнее пожалуйста.. ")









if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout) # При деплое закоментить
    asyncio.run(dp.start_polling(bot, skip_updates=False)) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей






























# async def main() -> None:
#     # Initialize Bot instance with default bot properties which will be passed to all API calls
#     bot = Bot(token=telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Markdown  HTML
#     # And the run events dispatching
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())