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
            f"<b>{DiceEmoji.DICE}Welcome to our bot!</b>\n\n"
            
            "This bot provides you the opportunity to send your posts "
            "to your favorite Telegram channels if they use it.\n\n"
            
            "If you're an admin of a Telegram channel, you can use this "
            "bot to allow your subscribers to send posts to your channel."
        ),
        reply_markup=builder.as_markup()
    )
