from aiogram import Dispatcher, types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot



async def quiz_2(call: types.CallbackQuery):
    markup2 = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("MORE", callback_data="quiz_2_button")
    markup2.add(button2)
    question = "The biggest country?"
    answer = [
        "USA",
        "China",
        "Canada",
        "Kyrgyzstan",
        "Russia"
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation="ДУМАЙ",
        open_period=10,
        reply_markup=markup2
    )


async def quiz_3(call: types.CallbackQuery):
    question = "What is the highest grossing film in history?"
    answer = [
        "Titanic",
        "Avengers",
        "Avatar",
        "Star Wars"
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="ДУМАЙ",
        open_period=10,

    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="quiz_button")
    dp.register_callback_query_handler(quiz_3, text="quiz_2_button")
