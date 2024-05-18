from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from send_analytics_bot.custom_filters.chat_types import (
    ChatTypeFilter,
    IsAdmin
)
from send_analytics_bot.keyboards.admin_keyboards import admin_keyboard, \
    AdminCommand, admin_cancel, admin_list_kb
from send_analytics_bot.states.admin_states import AdminStates

admins = [448260564, ]
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']),
                            IsAdmin(admins))


class AdminTG(StatesGroup):
    user_id = State()


@admin_router.message(StateFilter(None), Command('admin'))
async def admin_start(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.start)
    await message.answer('Выберите действие', reply_markup=admin_keyboard)


@admin_router.message(StateFilter(AdminStates), F.text == AdminCommand.cancel)
async def cancel_message(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await admin_start(message, state)


@admin_router.message(AdminStates.start, F.text == AdminCommand.add)
async def send_add_admin_message(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.add)
    await message.answer('Введите id пользователя TG',
                         reply_markup=admin_cancel)


@admin_router.message(AdminStates.add, F.text)
async def add_admin_by_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    if admin_id.isdigit():
        admins.append(int(admin_id))
        await message.answer('Админ добавлен.')
        await admin_start(message, state)
    else:
        await message.answer('Убедитесь в корректности id.')
        await send_add_admin_message(message, state)


@admin_router.message(AdminStates.start, F.text == AdminCommand.delete)
async def delete_admin_select(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.delete)
    await message.answer('Кого удаляем?',
                         reply_markup=admin_list_kb(admins))


@admin_router.message(AdminStates.delete, F.text)
async def delete_admin_by_id(message: types.Message, state: FSMContext):
    try:
        admins.remove(int(message.text))
        await message.answer(f'user {int(message.text)} удален')
        await admin_start(message, state)
    except Exception:
        await message.answer('Ошибка: выберите из списка',
                             reply_markup=admin_list_kb(admins))

# @admin_router.message(Command('admin'))
# async def admin_start(message: types.Message):
#     await message.answer(
#         f'Привет, <b>{message.from_user.first_name}</b>, xто хотите сделать?',
#         reply_markup=ADMIN_KB)
#
#
# @admin_router.message(F.text == 'Удалить администратора')
# async def admin_list(message: types.Message, session: AsyncSession):
#     for user in await orm_get_admins(session):
#         await message.answer(
#             user.username,
#             caption=f'<strong>{user.username}',
#
#             reply_markup=get_callback_btns(
#                 btns={
#                     'Удалить': f'delete_{user.id}',
#                     'Отмена': f'cancel_',
#                 }
#             ),
#         )
#     await message.answer("Список администраторов ⏫")
#     await message.answer('Выберите администратора для удаления',
#                          reply_markup=types.ReplyKeyboardRemove())
#
#
# @admin_router.message(F.text == 'Установка периода сбора данных')
# async def admin_list(message: types.Message, session: AsyncSession):
#     await message.answer('Укажите',
#                          reply_markup=get_callback_btns(
#                              btns={
#                                  '1 час': f'period_1 час',
#                                  '5 часов': f'period_5 часов',
#                                  '10 часов': f'period_10 часов',
#                                  '15 часов': f'period_15 часов',
#                                  '24 часa': f'period_24 часа',
#                              }
#                          )
#                          )
#
#
# @admin_router.callback_query(F.data.startswith('delete_'))
# async def delete_admin(callback: types.CallbackQuery, session: AsyncSession,
#                        state: FSMContext):
#     user_id = callback.data.split('_')[-1]
#     await orm_delete_admin(session, int(user_id))
#     await callback.answer('Администратор удален')
#     await callback.message.answer(f'Администратор удален!',
#                                   reply_markup=ADMIN_KB)
#
#
# @admin_router.callback_query(F.data.startswith('period_'))
# async def set_period_callback(callback: types.CallbackQuery,
#                               session: AsyncSession, state: FSMContext):
#     period = callback.data.split('_')[-1]
#     await callback.answer(f'Выбран период {period}')
#     await callback.message.answer(f'Вы выборали {period} !',
#                                   reply_markup=ADMIN_KB)
#     set = period.split(' ')[0]
#
#     # ПЕРЕДАЕМ ПАРЕМЕТР ПЕРИОДА ФУНКЦИИ
#     # ФУНКЦИЮ НУЖНО СОЗДАТЬ!
#     # await opros_bot(session, int(set))
#
#
# @admin_router.callback_query(F.data.startswith('cancel_'))
# async def delete_admin(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.answer('Отмена')
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.clear()
#     await callback.message.answer('Действие отменено!', reply_markup=ADMIN_KB)
#     return
#
#
# @admin_router.message(Command('admin'))
# async def admin_start(message: types.Message, bot: Bot):
#     await message.answer('Что хотите сделать?', reply_markup=ADMIN_KB)
#
#
# # Код ниже для машины состояний (FSM)
#
#
# @admin_router.message(StateFilter(None), F.text == 'Добавить администратора')
# async def add_new_admin(message: types.Message, state: FSMContext):
#     await message.answer(
#         'Ведите ID администратора', reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AdminTG.username)
#
#
# @admin_router.message(AdminTG.username, F.text)
# async def add_admin_name(message: types.Message, state: FSMContext,
#                          session: AsyncSession):
#     if len(message.text) >= 32:
#         await message.answer(
#             'Имя не должно превышать 32 символов. \n Введите заново')
#         return
#
#     await state.update_data(username=message.text, is_admin=True)
#
#     data = await state.get_data()
#     try:
#         await orm_add_admin(session, data)
#         await message.answer(
#             f'Администратор с ID {str(message.text)}, добавлен!',
#             reply_markup=ADMIN_KB)
#     except Exception as e:
#         await message.answer(
#             f'Ошибка: \n{str(e)}\nОбратись к программисту!',
#             reply_markup=ADMIN_KB,
#         )
#         await state.clear()
