import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.bot_db import sql_command_all_users
# from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from config import bot


async def limit_sitting(bot: Bot):
    users = await sql_command_all_users()
    for user in users:
        await bot.send_message(user[0], f'{user[-1]} , Лимит просмотра телефона исчерпан')


async def set_schedule():
    scheduler = AsyncIOScheduler(timezone="Asia / Bishkek")

    scheduler.add_job(
        limit_sitting,
        kwargs={"bot": bot},
        trigger=DateTrigger(
            run_date=datetime.datetime(month=5, day=2, year=2023)
        )
    )
    scheduler.start()
