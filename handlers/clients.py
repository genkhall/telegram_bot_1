from aiogram import Dispatcher, types
from config import bot, dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from aiogram.types import ContentType, Message
from database.bot_db import sql_command_random, sql_command_all_users, sql_command_insert_users
from utils import get_ids_from_users


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    users = await sql_command_all_users()
    ids = get_ids_from_users(users)
    if message.from_user.id not in ids:
        await sql_command_insert_users(
            message.from_user.id,
            message.from_user.id_from_user,
            message.from_user.name
        )
    await bot.send_message(message.from_user.id, f'Добро пожаловать {message.from_user.full_name}')


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


async def cmd_pin(message: types.Message):
    reply_message = message.reply_to_message
    if reply_message:
        await bot.pin_chat_message(chat_id=reply_message.chat.id, message_id=reply_message.message_id)


async def get_random_mentor():
    random_user = await sql_command_random()
    await bot.send_message(f'{random_user[1]}',
                           f'{random_user[2]}',
                           f'{random_user[3]}',
                           f'{random_user[4]}',
                           f'{random_user[5]}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(send_meme, commands=['mem'])
    dp.register_message_handler(cmd_pin, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(get_random_mentor, commands=['get'])
