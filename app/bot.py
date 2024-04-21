import logging
# При деплое раскоментить
# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
from worker_db import get_user_by_id, adding_user
from keys import telegram
import sys
import os
import asyncio
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
from datetime import datetime, timezone, timedelta
import uuid
from aiogram.utils.chat_action import ChatActionMiddleware




dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
#bot = Bot(telegram) #, default=types.DefaultBotProperties(parse_mode="Markdown")) # Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(token=telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Этот бот собирает ваши раходы и доходы, для того что бы разложить все в общую статистику. Анализ и статистика поможет вам оценить и контроллировать расходы.")
        # Preparing user data
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
        # Save user data
    get_user = await get_user_by_id(id)
    if get_user is None:
        push_data_user = {
            "id": id,
            "name": name,
            "full_name": full_name,
            "first_name": first_name,
            "last_name": last_name
        }
        await adding_user(push_data_user)
    else:
        print()
        logging.info(f"The user id:{id} is already in the database.")


    # MENU
    bot_commands = [
        BotCommand(command="/add", description="📈 Приход"),
        BotCommand(command="/dell", description="📉 Расход"),
        BotCommand(command="/bal", description="💵 Баланс"), 
        BotCommand(command="/stat", description="📊 Статистика"),
        BotCommand(command="/set", description="⚙️ Настройки"),
    ]
    await bot.set_my_commands(bot_commands)
    return


# Сделать что бы при открытии кнопок уже выдавало в названии кнопки сумму 

# SUB-MENU

class Form(StatesGroup):
    # Add
    add_cash = State() 
    add_cards = State()
    add_crypto = State()
    # Dell
    dell_cash = State()
    dell_cards = State()
    dell_crypto = State()


######## ADD MONEY ########
@dp.message(Command("add"))
async def menu_add(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Наличность", callback_data="add_cash")],
            [InlineKeyboardButton(text="💳 Банковские карты", callback_data="add_cards")],
            [InlineKeyboardButton(text="💸 Крипта", callback_data="add_crypto")],
        ]
    )
    await message.answer("📈 Выберите место куда добавляете деньги", reply_markup=keyboard)

# ADD MONEY --- cash
@dp.callback_query(lambda c: c.data == 'add_cash')
async def process_add_cash(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения наличности:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_cash)

@dp.message(Form.add_cash, F.content_type.in_({'text'}))
async def invoice_add_cash(message: Message, state: FSMContext):
    id = user_id(message)
    # user_uuid = uuid.uuid4()
    print(message.text)

    push_data_user = {
        "id": id,
        "name": name,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name
    }


    await state.clear()

# ADD MONEY --- card
@dp.callback_query(lambda c: c.data == 'add_cards')
async def process_add_cards(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения банковской карты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_cards)

@dp.message(Form.add_cards, F.content_type.in_({'text'}))
async def invoice_add_cards(message: Message, state: FSMContext):
    print(message.text)
    await state.clear()

# ADD MONEY --- add_crypto
@dp.callback_query(lambda c: c.data == 'add_crypto')
async def process_add_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения криптокошелька в USDT:") # {USDT}
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_cards)

@dp.message(Form.add_crypto, F.content_type.in_({'text'}))
async def invoice_add_crypto(message: Message, state: FSMContext):
    print(message.text)
    await state.clear()


######## DELL MONEY ########
@dp.message(Command("dell"))
async def menu_dell(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Наличность", callback_data="dell_cash")],
            [InlineKeyboardButton(text="💳 Банковские карты", callback_data="dell_cards")],
            [InlineKeyboardButton(text="💸 Крипта", callback_data="dell_crypto")],
        ]
    )
    await message.answer("📉 Выберите место откуда убыло", reply_markup=keyboard)

# DELL MONEY --- cash
@dp.callback_query(lambda c: c.data == 'dell_cash')
async def process_dell_cash(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите потраченую сумму наличности:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.dell_cash)

@dp.message(Form.dell_cash, F.content_type.in_({'text'}))
async def invoice_dell_cash(message: Message, state: FSMContext):
    print(message.text)
    await state.clear()

# DELL MONEY --- cards
@dp.callback_query(lambda c: c.data == 'dell_cards')
async def process_dell_cards(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите потраченую сумму с карты:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.dell_cards)

@dp.message(Form.dell_cards, F.content_type.in_({'text'}))
async def invoice_dell_cards(message: Message, state: FSMContext):
    print(message.text)
    await state.clear()

# DELL MONEY --- crypto
@dp.callback_query(lambda c: c.data == 'dell_crypto')
async def process_dell_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите потраченую сумму в криптовалюте:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.dell_crypto)

@dp.message(Form.dell_crypto, F.content_type.in_({'text'}))
async def invoice_dell_crypto(message: Message, state: FSMContext):
    print(message.text)
    await state.clear()




######## BALANS ########
@dp.message(Command("bal"))
async def menu_bal(message: types.Message):
    #id = user_id(message)
    await message.answer("Баланс")
    # await bot.answer_callback_query(message.id)
    # await message.answer("📈 Выберите место куда добавляете деньги", reply_markup=keyboard)



######## Statistic ########
@dp.message(Command("stat"))
async def menu_stat(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика за месяц", callback_data="stat_month")],
            [InlineKeyboardButton(text="📊 Статистика за год", callback_data="stat_year")],
            # [InlineKeyboardButton(text="📊 ", callback_data="add_crypto")],
        ]
    )
    await message.answer("📊 Выберите вариант статистики:", reply_markup=keyboard)

# STAT --- month
@dp.callback_query(lambda c: c.data == 'stat_month')
async def process_stat_month(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Статистика за месяц")
    await bot.answer_callback_query(callback_query.id)

# STAT --- year
@dp.callback_query(lambda c: c.data == 'stat_year')
async def process_stat_year(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Статистика за год")
    await bot.answer_callback_query(callback_query.id)



######## SETINGS ########
@dp.message(Command("set"))
async def menu_stat(message: types.Message):
    #id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Валюта", callback_data="currency")],
            [InlineKeyboardButton(text="Язык бота", callback_data="lang")],
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








@dp.message()
async def my_handler(message: Message):
    await typing(message)
    await asyncio.sleep(2)
    result = message.text
    print(result)
    await message.answer(result)



# @router.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")







if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) # При деплое закоментить
    asyncio.run(dp.start_polling(bot, skip_updates=False)) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей
































# async def main() -> None:
#     # Initialize Bot instance with default bot properties which will be passed to all API calls
#     bot = Bot(token=telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Markdown  HTML
#     # And the run events dispatching
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())