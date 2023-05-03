from aiogram import Dispatcher, types
from config import bot, ADMINS, API_KEY
import pyowm

owm = pyowm.OWM(API_KEY)


async def weather_command(message: types.Message):
    await message.reply("Введите город")


async def weather(message: types.Message):
    try:
        city = message.text
        observation = owm.weather_at_place(city)

        if observation is None:
            await message.reply(f"Информация о погоде для города {city} не найдена")
            return

        w = observation.get_weather()

        temperature = w.get_temperature('celsius')['temp']
        status = w.get_status()

        weather_message = f"Текущая температура в {city} - {temperature:.1f}°C\nСостояние погоды - {status}"

        await message.reply(weather_message)

    except Exception as e:
        await message.reply(f"Ошибка: {e}")


async def echo_message(message: types.Message):
    await bot.send_message("HI")


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(weather_command, commands=['weather'])
    dp.register_message_handler(weather)
    dp.register_message_handler(echo_message)
