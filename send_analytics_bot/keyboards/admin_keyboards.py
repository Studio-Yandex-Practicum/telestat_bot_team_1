import dataclasses

from aiogram import types


@dataclasses.dataclass
class AdminCommand:
    add = 'Добавить администратора'
    delete = 'Удалить администратора'
    cancel = 'Отменить'


admin_start_buttons = [
    [types.KeyboardButton(text=AdminCommand.add)],
    [types.KeyboardButton(text=AdminCommand.delete)]
]
admin_keyboard = types.ReplyKeyboardMarkup(keyboard=admin_start_buttons,
                                           resize_keyboard=True)

admin_cancel_buttons = [
    [types.KeyboardButton(text=AdminCommand.cancel, )]
]
admin_cancel = types.ReplyKeyboardMarkup(keyboard=admin_cancel_buttons,
                                         resize_keyboard=True)


async def admin_list_kb(admin_list: list[int]):
    keyboard = []
    for admin in admin_list[1::]:
        keyboard.append([types.KeyboardButton(text=str(admin))])
    keyboard.append([types.KeyboardButton(text=AdminCommand.cancel)])
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
