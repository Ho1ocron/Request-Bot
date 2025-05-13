from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData


class PostStates(StatesGroup):
    waiting_for_post = State()


class GroupCallback(CallbackData, prefix="group"):
    group_name: str
    gropu_id: int
