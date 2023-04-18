from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config import ADMINS
from . import clients_kb


# from client_kb import cancel_markup, submit_markup, start_markup
# from database.Bot_db import sql_command_insert
# =====================================================================================================================
class fsmAdminMentor(StatesGroup):
    ID = State()
    Name = State()
    Direction = State()
    Age = State()
    Group = State()
    submit = State()


# =====================================================================================================================

async def fsm_start(message: types.Message):
    if message.from_user.id not in ADMINS:  # Закреплять сообщения могут только админы
        await message.answer('Ты не админ!')

    else:
        await fsmAdminMentor.ID.set()
        await message.answer('ID ментора ?', reply_markup=clients_kb.cancel_markup)


async def load_ID(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['ID'] = message.text
    await fsmAdminMentor.next()
    await message.answer('Имя ментора ?')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Name'] = message.text
    await fsmAdminMentor.next()
    await message.answer('Направление ментора ?')


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Direction'] = message.text
    await fsmAdminMentor.next()
    await message.answer('Возраст ментора ?')


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Age'] = message.text
    await fsmAdminMentor.next()
    await message.answer('Группа ментора ?')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Group'] = message.text
        await message.answer(f"Информация о менторе: \n\n"
                             f"ID-ментора: {FSMCONTEXT_PROXY_STORAGE['ID']} \n"
                             f"Имя ментора: {FSMCONTEXT_PROXY_STORAGE['Name']} \n"
                             f"Направление ментора: {FSMCONTEXT_PROXY_STORAGE['Direction']} \n"
                             f"Возраст ментора: {FSMCONTEXT_PROXY_STORAGE['Age']} \n"
                             f"Группа ментора: {FSMCONTEXT_PROXY_STORAGE['Group']} \n")

    await fsmAdminMentor.next()
    await message.answer('Всё верно ?', reply_markup=clients_kb.submit_markup)


# =====================================================================================================================

async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        # await sql_command_insert(state)
        await message.answer('Готово!', reply_markup=clients_kb.start_markup)
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Ну ты и чорт конечно -_-', reply_markup=clients_kb.start_markup)
        await state.finish()


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Canceled',
                             reply_markup=clients_kb.start_markup)  # Чтоб после отмены сразу показывались все кнпопки


# =====================================================================================================================
def register_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True),
                                state='*')
    dp.register_message_handler(fsm_start, commands=['reg_mentor'])
    dp.register_message_handler(load_ID, state=fsmAdminMentor.ID)
    dp.register_message_handler(load_name, state=fsmAdminMentor.Name)
    dp.register_message_handler(load_direction, state=fsmAdminMentor.Direction)
    dp.register_message_handler(load_age, state=fsmAdminMentor.Age)
    dp.register_message_handler(load_group, state=fsmAdminMentor.Group)
    dp.register_message_handler(load_submit, state=fsmAdminMentor.submit)
