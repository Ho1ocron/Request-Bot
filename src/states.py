from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
import asyncio
from typing import List

class PostStates(StatesGroup):
    waiting_for_post = State()


class GroupCallback(CallbackData, prefix="group"):
    group_name: str
    group_id: int


message_to_forward: int | None = None
to_hide_name: bool = False


def set_hide_name(hide: bool) -> None:
    global to_hide_name
    to_hide_name = hide


def get_hide_name() -> bool:
    global to_hide_name
    return to_hide_name


def set_message_to_forward(message_id: int | None) -> None:
    global message_to_forward
    message_to_forward = message_id


def get_message_to_forward() -> tuple[int, bool] | tuple[None, None]:
    global message_to_forward, to_hide_name
    return message_to_forward, to_hide_name


media_group: List[int] = []


def save_media_group_messages(_media_group: List[int] | None) -> None:
    global media_group
    media_group = _media_group

def get_media_group_messages() -> List[int]:
    global media_group
    return media_group