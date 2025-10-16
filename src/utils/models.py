from aiogram.filters.callback_data import CallbackData


class GroupCallback(CallbackData, prefix="group"):
    group_name: str
    group_id: int
