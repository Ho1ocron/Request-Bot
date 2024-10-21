from aiogram import Router, F
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.types import Message
from aiogram.filters import Command
from utils import generate_base_deeplink
from aiogram.utils.deep_linking import create_start_link
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text
from keyboards import group_link_keyboard
from tortoise import Tortoise, run_async


router = Router(name=__name__)
router.message.filter(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
)


class Form(StatesGroup):
    sentence = State()


@router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
@router.message(F.content_type.in_({ContentType.GROUP_CHAT_CREATED, ContentType.SUPERGROUP_CHAT_CREATED}))
async def bot_added_to_group(message: Message) -> None:
    # Creating SuggestionChat with standart values, creating default deeplink
    # Sending success message
    # Open Settings of current SuggestionChat

    group_id = message.chat.id

    link_context = generate_base_deeplink(content=group_id) 
    link = await create_start_link(bot=message.bot, payload=group_id, encode=True) #: sending диклинк
    
    await message.answer(
        (
            "✔️ <b>Thank you for adding me to your group!</b>\n\n"

            "<i>To get more information and commands, use /help.</i>\n\n"

            "🔍<i>You can create your custom link with command /link.</i>\n\n"

            f"<b>Here is your link:</b> <code>{link}</code>\n\n"
        )
    )


@router.message(Command(commands=["link"]))
async def generate_deeplink(message: Message, state: FSMContext) -> None:
    # TODO: 1) add the ability to create custom links
    # 2) compare with the db if the link was already created and send that created link
    #  
    group_id = message.chat.id
    
    link_context = generate_base_deeplink(content=group_id) 
    link = await create_start_link(bot=message.bot, payload=group_id, encode=True)

    await state.set_state(Form.sentence)

    await message.answer(
        (
            "📝 Reply on this message with sending me a sentence you want to use in your link.\n\n"
            f"Your current link:\n<code>{link}</code>"
        )
    )
    

@router.message(Form.sentence)
async def process_sentence(message: Message, state: FSMContext) -> None:
    await state.update_data(sentence=message.text)
    data = await state.get_data()
    link = await create_start_link(message.bot, payload=data, encode=True)

    await state.clear()
    
    await message.answer(
        (
            "Alright, this will be your link:\n"
            f"<code>{link}</code>"
        )
    )


@router.message(Command(commands=["help"]))
async def help(message: Message) -> None:
    group_id = message.chat.id
    link = await create_start_link(message.bot, payload=group_id, encode=True)
    await message.answer(
        (
            "<i>🔍You can send your link again with command /link.</i>\n\n"

            f"<b>Your current link:</b>\n{link}\n\n"

            f"Group id: {message.chat.id}"
            
            ""
        )
    )