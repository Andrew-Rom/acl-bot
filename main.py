import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from puzzles import puzzle_math
from puzzles.acl_db import db_connection

logger = logging.getLogger(__name__)
file_log_format = '{levelname:<10} - {asctime:<20} - {funcName} - {msg}'
logging.basicConfig(filename='aclbot.log', filemode='a', encoding='UTF-8',
                    level=logging.INFO, style='{', format=file_log_format)

bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher()
router = Router()


def on_start():
    logger.info(msg='Bot started')
    print('Bot started')
    try:
        db_connection()
    except:
        print('Database did not create')

async def start_bot():
    dp.include_routers(router, puzzle_math.puzzle_router)
    dp.startup.register(on_start)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@router.message(Command('start'))
async def com_start(message: Message):
    bot_text = f'Hello, {message.from_user.first_name}!\n' \
               f'I am your bot!'
    await bot.send_message(message.from_user.id, text=bot_text)


@router.message(F.text.contains('bot'))
async def call_bot(message: Message):
    bot_text = f'{message.from_user.first_name}, I am still here!'
    await bot.send_message(message.from_user.id, text=bot_text)


# @router.message()
# async def nothing_to_do(message: Message):
#     bot_text = f'{message.from_user.first_name}, I do not know what you want!'
#     await bot.send_message(message.from_user.id, text=bot_text)


if __name__ == '__main__':
    asyncio.run(start_bot())
