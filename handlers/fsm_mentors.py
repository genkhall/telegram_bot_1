from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from config import ADMINS
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from . import clients_kb


class FSMAdminMentor(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def start_fsm(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не АДМИН!")
    else:
        await FSMAdminMentor.id.set()
        await message.answer("Напишите ваше ID", reply_markup=clients_kb.cancel_markup)


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.text
    await FSMAdminMentor.next()
    await message.answer("Как вас зовут?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdminMentor.next()
    await message.answer("Какое направление?", reply_markup=clients_kb.direction_markup)


async def load_direction(message: types.Message, state: FSMContext):
    if message.text not in ["BACKEND", "FRONT-END", "UX-UI DESIGN", "IOS", "ANDROID"]:
        await message.answer("Используй кнопки")
    else:
        async with state.proxy() as data:
            data["direction"] = message.text
        await FSMAdminMentor.next()
        await message.answer("Напишите возраст")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Ты человек?")
    elif not 10 < int(message.text) < 50:
        await message.answer("Уверен?")
    else:
        async with state.proxy() as data:
            data["age"] = message.text
        await FSMAdminMentor.next()
        await message.answer("Напишите свою группу", reply_markup=clients_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["group"] = message.text

        await message.answer(f"ID{data['id']}",
                             f"Имя:{data['name']} Направление: {data['direction']}"
                             f"Возраст ментора:{data['age']} Группа ментора:{data['group']}")
    await FSMAdminMentor.next()
    await message.answer("Проверьте данные", reply_markup=clients_kb.submit_markup)


async def submit_state(message: types.Message, state: FSMContext):
    if message.text.lower() == "все верно":

        await state.finish()
        await message.answer("Завершено", reply_markup=clients_kb.start_markup)
    elif message.text.lower() == "заново":
        await FSMAdminMentor.id.set()
        await message.answer("Напишите ваше ID")


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("See you soon!", reply_markup=clients_kb.start_markup)


def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(start_fsm, commands=['go'])
    dp.register_message_handler(load_id, state=FSMAdminMentor.id)
    dp.register_message_handler(load_name, state=FSMAdminMentor.name)
    dp.register_message_handler(load_direction, state=FSMAdminMentor.direction)
    dp.register_message_handler(load_age, state=FSMAdminMentor.age)
    dp.register_message_handler(load_group, state=FSMAdminMentor.group)
    dp.register_message_handler(submit_state, state=FSMAdminMentor.submit)

