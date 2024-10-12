from aiogram import F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums.chat_type import ChatType

from tortoise import Tortoise, run_async

from keyboards import main_keyboard, user_help_keyboard
from database import User, main

import logging



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_user(chat_id) -> None:
    await User.create(chat_id=chat_id)


router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.PRIVATE}),)


@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    chat_id = message.chat.id
    #await add_user(chat_id=chat_id)
    await message.answer(f"Your payload: {payload}")


@router.message(Command(commands=["start"]))
async def start(message: Message) -> None:
    keyboard = main_keyboard()
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

            "🔑 You can the channels that are available fow you with command /channels\n\n"

            "❔To get more information and commands, use /help.\n\n"

            f"{message.from_user.id}"
            
        ),
        reply_markup=keyboard.as_markup()
    )

    
@router.message(Command(commands=["channels"]))
async def channels(message: Message) -> None:
    await message.answer(
        (
            f"Channels:"
        )
    )


@router.message(Command(commands=["help"]))
async def help(message: Message) -> None:
    keyboard = user_help_keyboard()

    await message.answer(
        (
            f"✅ I'll help you, what are you looking for?"
        ),
        reply_markup=keyboard
        # Кнопка, которая будет присылать список всех доступных команд для пользователя, и их пояснение
        # Кнопка, которая будет предоставлять инфу о боте | об админах итп
        # callback data писать в callback_handlers.py
        # https://mastergroosha.github.io/aiogram-3-guide/buttons/
    )