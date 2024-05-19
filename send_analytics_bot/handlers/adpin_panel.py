from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from send_analytics_bot.custom_filters.chat_types import (
    ChatTypeFilter,
    IsAdmin
)
from send_analytics_bot.keyboards.admin_keyboards import (admin_keyboard,
                                                          AdminCommand,
                                                          admin_cancel,
                                                          admin_list_kb)
from send_analytics_bot.services.conf import admin_conf
from send_analytics_bot.states.admin_states import AdminStates

admins = [admin_conf.superuser, ]
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']),
                            IsAdmin(admins))


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
    await message.answer('Введите id.',
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
                         reply_markup=await admin_list_kb(admins))


@admin_router.message(AdminStates.delete, F.text)
async def delete_admin_by_id(message: types.Message, state: FSMContext):
    try:
        admins.remove(int(message.text))
        await message.answer(f'Админ {int(message.text)} удален')
        await admin_start(message, state)
    except Exception:
        await message.answer('Выберите пользователя из списка.',
                             reply_markup=await admin_list_kb(admins))
