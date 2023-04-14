from aiogram import Dispatcher, types
from config import bot
import random
from aiogram.types import ContentType, Message


async def echo(message: types.Message):
    if message.text.isdigit():
        square = int(message.text) ** 2
        await message.answer(str(square))
    else:
        await message.answer(message.text)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
