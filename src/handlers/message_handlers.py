from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.chat_type import ChatType
from keyboards import create_keyboard


router = Router(name=__name__)
router.message.filter(
    F.chat.type.in_({ChatType.PRIVATE}),
)


@router.message(Command(commands=["start"]))
async def start(message: Message) -> None:
    key_board = create_keyboard(text="📎 Add to your group", callback_data="https://t.me/ilovethissomuchbot?startgroup=true")
    #builder = InlineKeyboardBuilder()
    #builder.row(types.InlineKeyboardButton(text="📎 Add to your group", url=""))
    # -> keyboards.py
    
    # https://t.me/bot?startgroup=true
    # https://t.me/ilovethissomuchbot?startgroup=true
    
    
    await message.answer(
        (
            f"👋 <b>Welcome to our bot!</b> 👋\n\n"
            
            "💡This bot provides you the opportunity to <b>send your posts</b> "
            "to your favorite Telegram <b>channels</b> if they use it.\n\n"
            
            "💭<i>If you're an admin of a Telegram channel, you can use this</i> "
            "<i>bot to allow your subscribers to send posts to your channel.</i>\n\n"

            "❔<i>To get more information and commands, use /help.</i>\n\n"
        ),
        reply_markup=key_board.as_markup()
    )



@router.message(Command(commands=["help"]))
async def help(message: Message) -> None:
    await message.answer(
        (
            f"I'll help you, what are you looking for?"
        )
        # Кнопка, которая будет присылать список всех доступных команд для пользователя, и их пояснение
        # Кнопка, которая будет предоставлять инфу о боте | об админах итп
        # callback data писать в callback_handlers.py
        # https://mastergroosha.github.io/aiogram-3-guide/buttons/
    )