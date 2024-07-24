from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types



def create_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Add to your group", callback_data="random_value"))
    return builder
