from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_admin,
    orm_get_admins,
    orm_delete_admin
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    'Добавить администратора',
    'Удалить администратора',
    'Выбрать телеграм канал',
    'Установка периода сбора данных',
    placeholder='Выберите действие',
    sizes=(2, 2),
)

SET_PERIOD_KB = get_keyboard(
    '1 час',
    '5 часов',
    '10 часов',
    '15 часов',
    '24 часа',
    'Отменить действие',
    placeholder='Выберите интервал',
    sizes=(2, 3, 1),
)



class AdminTG(StatesGroup):
    username = State()


@admin_router.message(Command('admin'))
async def admin_start(message: types.Message):
    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>, xто хотите сделать?', reply_markup=ADMIN_KB)


@admin_router.message(F.text == 'Удалить администратора')
async def admin_list(message: types.Message, session: AsyncSession):
    for user in await orm_get_admins(session):
        await message.answer(
            user.username,
            caption=f'<strong>{user.username}',

            reply_markup=get_callback_btns(
                btns={
                    'Удалить': f'delete_{user.id}',
                    'Отмена': f'cancel_',
                }
            ),
        )
    await message.answer("Список администраторов ⏫")
    await message.answer('Выберите администратора для удаления',
                         reply_markup=types.ReplyKeyboardRemove())


@admin_router.message(F.text == 'Установка периода сбора данных')
async def admin_list(message: types.Message, session: AsyncSession):
    await message.answer('Укажите',
                         reply_markup=get_callback_btns(
                             btns={
                                 '1 час': f'period_1 час',
                                 '5 часов': f'period_5 часов',
                                 '10 часов': f'period_10 часов',
                                 '15 часов': f'period_15 часов',
                                 '24 часa': f'period_24 часа',
                             }
                         )
                         )

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_admin(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    user_id = callback.data.split('_')[-1]
    await orm_delete_admin(session, int(user_id))
    await callback.answer('Администратор удален')
    await callback.message.answer(f'Администратор удален!', reply_markup=ADMIN_KB)


@admin_router.callback_query(F.data.startswith('period_'))
async def set_period_callback(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    period = callback.data.split('_')[-1]
    await callback.answer(f'Выбран период {period}')
    await callback.message.answer(f'Вы выборали {period} !', reply_markup=ADMIN_KB)
    set = period.split(' ')[0]

    # ПЕРЕДАЕМ ПАРЕМЕТР ПЕРИОДА ФУНКЦИИ
    # ФУНКЦИЮ НУЖНО СОЗДАТЬ!
    # await opros_bot(session, int(set))








@admin_router.callback_query(F.data.startswith('cancel_'))
async def delete_admin(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Отмена')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.answer('Действие отменено!', reply_markup=ADMIN_KB)
    return


@admin_router.message(Command('admin'))
async def admin_start(message: types.Message, bot: Bot):
    await message.answer('Что хотите сделать?', reply_markup=ADMIN_KB)


# Код ниже для машины состояний (FSM)


@admin_router.message(StateFilter(None), F.text == 'Добавить администратора')
async def add_new_admin(message: types.Message, state: FSMContext):
    await message.answer(
        'Ведите ID администратора', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AdminTG.username)


@admin_router.message(AdminTG.username, F.text)
async def add_admin_name(message: types.Message, state: FSMContext, session: AsyncSession):
    if len(message.text) >= 32:
        await message.answer('Имя не должно превышать 32 символов. \n Введите заново')
        return

    await state.update_data(username=message.text, is_admin=True)

    data = await state.get_data()
    try:
        await orm_add_admin(session, data)
        await message.answer(
            f'Администратор с ID {str(message.text)}, добавлен!', reply_markup=ADMIN_KB)
    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}\nОбратись к программисту!',
            reply_markup=ADMIN_KB,
        )
        await state.clear()
