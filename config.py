from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
ADMINS = (701534660,)

TOKEN = config("TOKEN")
API_KEY = config("API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

