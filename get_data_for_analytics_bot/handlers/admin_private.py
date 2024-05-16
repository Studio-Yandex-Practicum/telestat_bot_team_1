from aiogram import F, Router, types, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_admin,
    orm_get_admins,
    orm_delete_admin, orm_period_parsing, orm_get_channel, orm_update_channel
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

router = Router()  # [1]

dp = Dispatcher()

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


class ChannelTG(StatesGroup):
    channel_id = State()
    channel_name = State()
    channel_current = State()


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


@admin_router.message(F.text == 'Выбрать телеграм канал')
async def choice_telegram_channel(message: types.Message, state: FSMContext, session: AsyncSession):
    if len(await orm_get_channel(session)) == 0:
        await message.answer('Вы еще не добавили каналы, пройдите в канал и выполните команду "/add"')
        return
    else:
        for channel in await orm_get_channel(session):
            await message.answer(
                channel.channel_name,
                caption=f'<strong>{channel.channel_name}',

                reply_markup=get_callback_btns(
                    btns={
                        'Выбрать': f'channel-{channel.channel_name}',
                        'Отмена': f'cancel_',
                    }
                ),
            )
        await message.answer("Список каналов ⏫")
        await message.answer('Выберите канал для анализа данных',
                             reply_markup=types.ReplyKeyboardRemove())


@admin_router.message(F.text == 'Установка периода сбора данных')
async def admin_list(message: types.Message):
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
async def set_period_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    period = callback.data.split('_')[-1]
    await callback.answer(f'Выбран период {period}')
    await callback.message.answer(f'Вы выбрали {period} !', reply_markup=ADMIN_KB)
    period = period.split(' ')[0]
    await state.update_data(period_id=1, period=period)
    data = await state.get_data()
    await orm_period_parsing(session, data)
    # ПЕРЕДАЕМ ПАРЕМЕТР ПЕРИОДА ФУНКЦИИ
    # ФУНКЦИЮ НУЖНО СОЗДАТЬ!
    # В БД вносится текущий параметр, для выбора периода брать
    # последнее добавленное значение


@admin_router.callback_query(F.data.startswith('cancel_'))
async def delete_admin(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Отмена')
    await state.clear()
    await callback.message.answer('Действие отменено!', reply_markup=ADMIN_KB)
    return


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
    print(data)
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


@admin_router.callback_query(F.data.startswith('channel-'))
async def set_period_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    channel = callback.data.split('-')[-1]
    for choice in await orm_get_channel(session):  # нет выбранных каналов (ОБНУЛИЛ ПЕРЕД ВЫБОРОМ).
        if choice.channel_current is True:
            channel_id = choice.id
            await state.update_data(channel_current=False)
            data = await state.get_data()
            await orm_update_channel(session, channel_id, data)
            break

    for choice in await orm_get_channel(session):  # ставим статус True выбранному каналу.
        if choice.channel_name == channel:
            channel_id = choice.id
            await state.update_data(channel_current=True)
            data = await state.get_data()
            await orm_update_channel(session, channel_id, data)
            print('Выбор сделан')
    await callback.answer(f'Выбран канал {channel}')
    await callback.message.answer(f'Вы выбрали {channel} !', reply_markup=ADMIN_KB)
