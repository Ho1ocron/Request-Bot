from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router(name=__name__)


@router.message(Command(commands=["start", "help"]))
async def start(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Add to your group", callback_data="random_value"))
    # -> keyboards.py
    
    # https://t.me/bot?startgroup=true
    
    
    await message.answer(
        (
            "<b>Welcome to our bot!</b>\n\n"
            
            "This bot provides you the opportunity to send your posts "
            "to your favorite Telegram channels if they use it.\n\n"
            
            "If you're an admin of a Telegram channel, you can use this "
            "bot to allow your subscribers to send posts to your channel."
        ),
        reply_markup=builder.as_markup()
    )
