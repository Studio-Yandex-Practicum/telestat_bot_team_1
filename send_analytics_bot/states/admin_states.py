from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    start = State()
    add = State()
    delete = State()
