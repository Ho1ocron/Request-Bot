from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


#def create_keyboard(text: str, callback_data: Optional[str] = None, url: Optional[str] = None) -> InlineKeyboardBuilder:
#    builder = InlineKeyboardBuilder()
#    builder.add(InlineKeyboardButton(text=text, callback_data=callback_data, url=url))
#    return builder


def create_keyboard(*args: InlineKeyboardButton) -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder().add(*args)

