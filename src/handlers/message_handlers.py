from aiogram import F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums.chat_type import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_media_group import media_group_handler
from typing import List
from states import save_media_group_messages, set_hide_name, set_message_to_forward, PostStates
from database import create_user, get_users_groups, get_user, get_group
from keyboards import main_keyboard, user_help_keyboard
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.PRIVATE}),)


@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    group_id = int(decode_payload(command.args))
    user_id = int(message.from_user.id)
    name = message.from_user.first_name

    group = await get_group(group_id=group_id)
    await create_user(user_id=user_id, name=name, group_id=group_id)
    # await state.set_state(PostStates.waiting_for_post)
    await message.answer(
        (
            f"✅ Now, you can send your posts to this channel: <b>{group.name}</b>!\n\n"
            f"Attention! By default, the bot will send your posts to the channel without hiding your name.\n\n"
            f"If you want to hide your name, use the command /hide_name.\n\n"
            f"To unhide it, use the command /unhide_name.\n\n"
        )
    )



@router.message(Command(commands=["start"]))    
async def start(message: Message) -> None:
    bot_name = await message.bot.get_me()
    keyboard = main_keyboard(bot_name=bot_name.username)

    await message.answer(
        (
            f"👋 <b>Welcome to our bot!</b> 👋\n\n"
            
            "💡This bot provides you the opportunity to <b>send your posts</b> "
            "to your favorite Telegram <b>channels</b> if they use it.\n\n"
            
            "💭<i>If you're an admin of a Telegram channel, you can use this</i> "
            "<i>bot to allow your subscribers to send posts to your channel.</i>\n"
            "Add this bot to your admin's group where your followers will send their posts.\n"
            "❕<b>Please make sure that your group's name matches exactly your Telegram channel's name</b>❕\n\n"

            "🔑 You can view the channels that are available for you with command /channels\n\n"

            "❔To get more information and commands, use /help.\n\n"
            
        ),
        reply_markup=keyboard.as_markup()
    )

    
@router.message(Command(commands=["channels"]))
async def channels(message: Message) -> None:
    groups = await get_users_groups(user_id=int(message.from_user.id))
    await message.answer(
        (
            f"Channels available for you: {", ".join(groups)}"
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


@router.message(Command(commands=["info"]))
async def test(message: Message) -> None:
    user = await get_user(user_id=int(message.from_user.id))
    await message.answer(
        (
            f"id: {user.id}\n"
            f"username: {user.name}\n"
            f"groups: {user.list_of_channels}"
        )
    )


@router.message(Command(commands=["hide_name"]))
async def hide_name(message: Message) -> None:
    set_hide_name(True)
    await message.answer(
        (
            "✅ From now on, your name will be hidden when you send posts to the channel."
        )
    )
@router.message(Command(commands=["unhide_name"]))
async def unhide_name(message: Message) -> None:
    set_hide_name(False)
    await message.answer(
        (
            "✅ From now on, your name will be visible when you send posts to the channel."
        )
    )


@router.message(~F.text.startswith("/"), ~F.media_group_id)
async def receive_post(message: Message, state: FSMContext) -> None:    
    user_id = int(message.from_user.id)
    user_groups, user_groups_ids = await get_users_groups(user_id=user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=group, callback_data=f"select_group:{group_id}")]
            for group, group_id in zip(user_groups, user_groups_ids)
        ] + [
            [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
        ]
    )
    set_message_to_forward(message=message)
    await message.answer(
        "Please select a channel:",
        reply_markup=keyboard
    )
    
    # await message.answer(
    #     (
    #         "✅ Choose a channel where you want to send your post:"
    #     )
    # )
    
# пофиксить чтобы фотки были в правильном порядке, а не в рандомном
@router.message(PostStates.waiting_for_post, ~F.text.startswith("/"), F.media_group_id)
@media_group_handler # Copied and imported as lib from https://github.com/deptyped/aiogram-media-group It just works. 
async def album_handler(messages: List[Message], state: FSMContext) -> None:
    user_groups, user_groups_ids = await get_users_groups(user_id=int(messages[0].from_user.id))
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=group, callback_data=f"select_group:{group_id}")]
            for group, group_id in zip(user_groups, user_groups_ids)
        ] + [
            [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
        ]
    )
    await messages[-1].answer(
        "Please select a channel:",
        reply_markup=keyboard
    )
    
    save_media_group_messages(_media_group=messages)