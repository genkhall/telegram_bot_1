from aiogram import Bot, Dispatcher
from decouple import config


TOKEN = config("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
ADMINS = (701534660,)
