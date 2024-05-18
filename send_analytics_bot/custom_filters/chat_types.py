from aiogram import Bot, types
from aiogram.filters import Filter


from send_analytics_bot.keyboards.admin_keyboards import admin_keyboard
from send_analytics_bot.states.admin_states import AdminStates


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        if message.from_user.id not in self.admin_ids:
            await message.answer('К сожалению, у вас нет прав доступа.')
            return False
        return True
