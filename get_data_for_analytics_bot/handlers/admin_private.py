from aiogram import F, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    'Выбор Telegram-канала',
    'Установка периода сбора данных',
    'Добавить администратора',
    'Удалить администратора',
    placeholder='Выберите действие',
    sizes=(2, 2),
)


@admin_router.message(Command('admin'))
async def admin(message: types.Message):
    await message.answer('Что хотите сделать?', reply_markup=ADMIN_KB)


@admin_router.message(F.text == 'Выбор Telegram-канала')
async def choice_tg_ch(message: types.Message):
    await message.answer('Выбор Telegram-канала')


@admin_router.message(F.text == 'Установка периода сбора данных')
async def set_collect_data(message: types.Message):
    await message.answer('Установка периода сбора данных')


@admin_router.message(F.text == 'Добавить администратора')
async def add_admin(message: types.Message):
    await message.answer('Добавить администратора')


async def del_admin(message: types.Message):
    await message.answer('Удалить администратора')


# Код ниже для машины состояний (FSM)

@admin_router.message(F.text == 'Добавить товар')
async def add_product(message: types.Message):
    await message.answer(
        'Введите название товара', reply_markup=types.ReplyKeyboardRemove()
    )


@admin_router.message(Command('отмена'))
@admin_router.message(F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message) -> None:
    await message.answer('Действия отменены', reply_markup=ADMIN_KB)


@admin_router.message(Command('назад'))
@admin_router.message(F.text.casefold() == 'назад')
async def cancel_handler(message: types.Message) -> None:
    await message.answer(f'ок, вы вернулись к прошлому шагу')


@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer('Введите описание товара')


@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer('Введите стоимость товара')


@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer('Загрузите изображение товара')


@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer('Товар добавлен', reply_markup=ADMIN_KB)
