from aiogram import Router, F
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.types import Message
from aiogram.filters import Command
from utils import generate_base_deeplink
from aiogram.utils.deep_linking import create_start_link


router = Router(name=__name__)
router.message.filter(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
)


@router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
@router.message(F.content_type.in_({ContentType.GROUP_CHAT_CREATED, ContentType.SUPERGROUP_CHAT_CREATED}))
async def bot_added_to_group(message: Message) -> None:
    # Creating SuggestionChat with standart values, creating default deeplink
    # Sending success message
    # Open Settings of current SuggestionChat

    group_id = message.chat.id

    link_context = generate_base_deeplink(group_id=group_id) 
    link = await create_start_link(message.bot, link_context, encode=True)
    
    await message.answer(
        (
            "✔️<b>Thank you for adding me to your group!</b>\n\n"

            "🪄Now, I will create <b>a link you can send to your subscribers</b> so they can use me for sending suggestions to you.\n\n"

            "<i>To get more information and commands, use /help.</i>\n\n"

            f"<b>Here is your link:</b> <code>{link}</code>\n\n"
        )
    )


@router.message(Command(commands=["link"]))
async def generate_deeplink(message: Message) -> None:
    # TODO: 1) add the ability to create custom links
    # 2) compare with the db if the link was already created and send that created link
    #  
    group_id = message.chat.id
    
    link_context = generate_base_deeplink(group_id=group_id) 
    link = await create_start_link(message.bot, link_context, encode=True)

    await message.answer(f"<code>{link}</code>")
    

@router.message(Command(commands=["help"]))
async def help(message: Message) -> None:
    await message.answer(
        (
            ""
            ""
            ""
        )
    )