from aiogram.utils import executor

import logging
from config import dp, ADMINS, bot
from handlers import clients, fsm_mentors, extra, admin, callback
from database.bot_db import sql_create

clients.register_handlers_client(dp)
callback.register_handlers_callback(dp)
fsm_mentors.register_mentor(dp)
admin.register_handlers_admin(dp)
extra.register_handlers_extra(dp)


async def on_startup(dp):
    sql_create()
    await bot.send_message(ADMINS[0], "Все готовооо!")


async def on_shutdown(dp):
    await bot.send_message(ADMINS[0], "Бот покинул чат")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True,
                           timeout=5,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown
                           )


