from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types



def create_keyboard(text: str, callback_data: str):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    return builder
