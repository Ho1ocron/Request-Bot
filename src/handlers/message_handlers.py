from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.chat_type import ChatType
from aiogram.types.dice import DiceEmoji


router = Router(name=__name__)
router.message.filter(
    F.chat.type.in_({ChatType.PRIVATE}),
)


@router.message(Command(commands=["start"]))
async def start(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Add to your group", url="https://t.me/ilovethissomuchbot?startgroup=true"))
    # -> keyboards.py
    
    # https://t.me/bot?startgroup=true
    # https://t.me/ilovethissomuchbot?startgroup=true
    
    
    await message.answer(
        (
            f"👋 <b>Welcome to our bot!</b> 👋\n\n"
            
            "💡This bot provides you the opportunity to <b>send your posts</b> "
            "to your favorite Telegram <b>channels</b> if they use it.\n\n"
            
            "🗯<i>If you're an admin of a Telegram channel, you can use this</i> "
            "<i>bot to allow your subscribers to send posts to your channel.</i>"
        ),
        reply_markup=builder.as_markup()
    )
