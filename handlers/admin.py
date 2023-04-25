from database.bot_db import sql_command_all, sql_command_delete
from config import ADMINS, bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:  # Закреплять сообщения могут только админы
        await message.answer('Ты не админ!')
    else:
        users = await sql_command_all()
        for user in users:
            await bot.send_message(f'{user[1]}',
                                   f'{user[2]}',
                                   f'{user[3]}',
                                   f'{user[4]}',
                                   f'{user[5]}', reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        f'DELETE {user[2]}',
                        callback_data=f'delete{user[0]}'
                    )
                ))


async def complete_delete(call: types.CallbackQuery):
    id_user = call.data.replace("delete ", "")
    await sql_command_delete(id_user)
    await call.answer(text=f"Удалена запись с айди {id_user}",
                      show_alert=True)
    await call.message.delete()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_message_handler(complete_delete,
                                lambda call: call.data and call.data.startswith("delete"))
