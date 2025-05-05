from aiogram import F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums.chat_type import ChatType
from database.actions import create_user, check_user_exists, get_users_groups, get_user
from keyboards import main_keyboard, user_help_keyboard, choose_channel
from aiogram.fsm.state import State, StatesGroup
from states import PostStates
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# async def add_user(user_id: int, username: str, group_id: int) -> None:
#    await init_db()
#    user = await User.create(id=user_id, name=username)

#    if user.related_chat_id_list is None:
#        user.related_chat_id_list = [group_id]
#    else:
#        user.related_chat_id_list.append(group_id)
#    await close_db()


router = Router(name=__name__)
router.message.filter(F.chat.type.in_({ChatType.PRIVATE}),)


@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    group_id = int(decode_payload(command.args))
    user_id = int(message.from_user.id)
    username = message.from_user.first_name

    await create_user(user_id=user_id, username=username, group_id=group_id)
    await state.set_state(PostStates.waiting_for_post)
    if await check_user_exists(user_id=message.chat.id):
        await message.answer(
            (
                "You're already in, buddy!"
            )
        )
        return
    
    await message.answer(
        (
            f"✅ Now, you can send your posts to this channel: "
            f"channel name" #: Добавить название тгк сюда, куда юзер будет кидать посты
        )
    )



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
            f"Channels: {", ".join(groups)}"
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

@router.message(PostStates.waiting_for_post, ~F.text.startswith("/"))
async def receive_post(message: Message, state: FSMContext) -> None:
    user_groups = await get_users_groups(user_id=int(message.from_user.id))
    keyboard = choose_channel(groups=user_groups)
    await message.answer(
        (
            "✅ Choose a channel where you want to send your post:"
        ),
        reply_markup=keyboard
    )
    await state.clear()
    await state.set_state(PostStates.waiting_for_post)