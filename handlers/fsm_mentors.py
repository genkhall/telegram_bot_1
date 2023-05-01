from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config import ADMINS
from . import client_kb
from database.bot_db import sql_command_insert


# =====================================================================================================================
class FsmAdminMentor(StatesGroup):
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
        await FsmAdminMentor.ID.set()
        await message.answer('ID ментора ?', reply_markup=client_kb.cancel_markup)


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['ID'] = message.text
    await FsmAdminMentor.next()
    await message.answer('Имя ментора ?')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Name'] = message.text
    await FsmAdminMentor.next()
    await message.answer('Направление ментора ?')


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Direction'] = message.text
    await FsmAdminMentor.next()
    await message.answer('Возраст ментора ?')


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as FSMCONTEXT_PROXY_STORAGE:
        FSMCONTEXT_PROXY_STORAGE['Age'] = message.text
    await FsmAdminMentor.next()
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

    await FsmAdminMentor.next()
    await message.answer('Всё верно ?', reply_markup=client_kb.submit_markup)


# =====================================================================================================================

async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await sql_command_insert(state)
        await message.answer('Успешно добавлено!', reply_markup=client_kb.start_markup)
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Давай начнем все с начала', reply_markup=client_kb.start_markup)
        await state.finish()
    else:
        await message.answer("ошибка")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Canceled', reply_markup=client_kb.start_markup)



# =====================================================================================================================
def register_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True),
                                state='*')
    dp.register_message_handler(fsm_start, commands=['reg_mentor'])
    dp.register_message_handler(load_id, state=FsmAdminMentor.ID)
    dp.register_message_handler(load_name, state=FsmAdminMentor.Name)
    dp.register_message_handler(load_direction, state=FsmAdminMentor.Direction)
    dp.register_message_handler(load_age, state=FsmAdminMentor.Age)
    dp.register_message_handler(load_group, state=FsmAdminMentor.Group)
    dp.register_message_handler(load_submit, state=FsmAdminMentor.submit)
