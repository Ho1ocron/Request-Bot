from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message


class PostStates(StatesGroup):
    waiting_for_post = State()


class GroupCallback(CallbackData, prefix="group"):
    group_name: str
    gropu_id: int


message_to_forward: int | None


def set_message_to_forward(message_id: int | None) -> None:
    global message_to_forward
    message_to_forward = message_id


def get_message_to_forward() -> int | None:
    global message_to_forward
    return message_to_forward