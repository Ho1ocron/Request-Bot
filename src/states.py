from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message   
from typing import List, Optional

class PostStates(StatesGroup):
    waiting_for_post = State()


class GroupCallback(CallbackData, prefix="group"):
    group_name: str
    group_id: int


class BotState:
    def __init__(self):
        self._to_hide_name: bool = False
        self._message_to_forward: Optional[Message] = None
        self._media_group: List[int] = []

    # Hide name state
    def set_hide_name(self, hide: bool) -> None:
        self._to_hide_name = hide

    def get_hide_name(self) -> bool:
        return self._to_hide_name

    # Message forwarding state
    def set_message_to_forward(self, message: Optional[Message]) -> None:
        self._message_to_forward = message

    def get_message_to_forward(self) -> Optional[Message]:
        return self._message_to_forward

    # Media group state
    def set_media_group_messages(self, media_group: Optional[List[int]]) -> None:
        self._media_group = media_group or []

    def get_media_group_messages(self) -> List[int]:
        return self._media_group


bot_state = BotState()