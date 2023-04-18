from aiogram import Dispatcher, types
from config import bot, ADMINS
import random



#
#
# async def send_emoji(message: types.Message):
#     if message.from_user.id not in ADMINS:
#         await message.answer("Ты не мой хозяин!")
#     elif message.text.startswith('game'):
#         a = ['⚽️', '🎰', '🏀', '🎯', '🎳', '🎲']
#         b = random.choice(a)
#
#         await bot.send_dice(message.chat.id, emoji=b)
#
#
# def register_handlers_admin(dp: Dispatcher):
#     dp.register_message_handler(send_emoji)
