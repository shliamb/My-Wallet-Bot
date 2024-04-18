import logging
# При деплое раскоментить
# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл

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
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name

    # MENU
    bot_commands = [
        BotCommand(command="/add", description="📈 Приход"),
        BotCommand(command="/dell", description="📉 Расход"),
        BotCommand(command="/stat", description="📊 Статистика"),
        BotCommand(command="/set", description="⚙️ Настройки"),  # 💵
    ]
    await bot.set_my_commands(bot_commands)
    return




############################# SUB-MENU ######################################
#                                                                           #

# ADD MONEY
@dp.message(Command("add"))
async def admin(message: types.Message):
    id = user_id(message)
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
async def process_sub_admin_stat(callback_query: types.CallbackQuery):

    await bot.send_message(callback_query.from_user.id, "Вы проебали весь нал..")
    await bot.answer_callback_query(callback_query.id)




# DELL MONEY
@dp.message(Command("dell"))
async def admin(message: types.Message):
    id = user_id(message)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Наличность", callback_data="dell_cash")],
            [InlineKeyboardButton(text="💳 Банковские карты", callback_data="dell_cards")],
            [InlineKeyboardButton(text="💸 Крипта", callback_data="dell_crypto")],
        ]
    )
    await message.answer("📉 Выберите место откуда убыло", reply_markup=keyboard)




#                                                                           #
############################# SUB-MENU ######################################








# @dp.message()
# async def my_handler(message: Message):
#     await typing(message)
#     await asyncio.sleep(2)
#     result = message.text
#     print(result)
#     await message.answer(result)



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