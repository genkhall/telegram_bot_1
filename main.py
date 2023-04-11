from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from decouple import config
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from aiogram.types import ContentType, Message

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f'Добро пожаловать {message.from_user.full_name}')
    # await message.answer(f'Это тоже {message.from_user.full_name}')


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("ONE MORE", callback_data="quiz_button")
    markup.add(button)
    question = "The best IT courses?"
    answer = [
        "Codify",
        "GEEKS",
        "Peaksoft",
        "Makers",
        "Ogogo"
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="ДУМАЙ",
        reply_markup=markup,
        open_period=10
    )


@dp.callback_query_handler(text='quiz_button')
async def quiz_2(call: types.CallbackQuery):
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

    )


@dp.message_handler(text='/mem')
async def send_meme(message: Message):
    mem_file_id = [
        'https://st.europaplus.ru/mf/p/230472/news/370/037025/content/7a0d2186bf2dbc85631b9d7e49465fc4.jpg',
        'https://ichef.bbci.co.uk/news/640/cpsprodpb/6A6A/production/_122524272_688565d8-3c0f-4c76-b76d-4eb29801b475.jpg',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzAIJprAjjrU-TNO98Oyzf--qkaojQeR9oaQ&usqp=CAU',
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCVm-0CmUuqtqsLrWAYuYZrhUMJqC9p1yYsw&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSywhoMMlaDzD-X5TFRr0XV0xg0JbvcMdUx3Q&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYn6pRbq_jmNj3LioSTnnm6nx6uqW3gys8XA&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMEfCtca-rgrWW4c5Ay95TA0C-5gXUTBPdLQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRp94fXrC0aFg9LIJyMrDnewQ1wBg7qo_9fyQ&usqp=CAU"

    ]
    random_mem = random.choice(mem_file_id)
    await dp.bot.send_message(chat_id=message.from_user.id, text=random_mem)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        square = int(message.text) ** 2
        await message.answer(str(square))
    else:
        await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
