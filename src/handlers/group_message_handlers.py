from aiogram import Router, F
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link
from aiogram.types import ChatMemberUpdated
from aiogram.enums.chat_member_status import ChatMemberStatus

from database import create_group



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
    group_name = message.chat.title
    link = await create_start_link(bot=message.bot, payload=group_id, encode=True) #: sending диклинк

    await create_group(group_id=group_id, name=group_name)
    
    await message.answer(
        (
            "✔️ <b>Thank you for adding me to your group!</b>\n\n"

            "<b>❕Please, make sure this group's name matches exactly to the name of your Telegram channel❕</b>\n"

            "If it isn't, rename your group and then use command /update.\n\n"

            "<i>To get more information and commands, use /help.</i>\n\n"

            "🔍<i>You can create your custom link with command /link.</i>\n\n"

            f"<b>Here is your link</b>: <code>{link}</code>"
        ),
        #reply_markup=keyboard
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


@router.message(F.new_chat_title)
async def title_changed(message: Message) -> None:
    new_title = message.new_chat_title
    chat_id = message.chat.id
    admin_list = [] # Do not forget to change it
    await create_group(group_id=chat_id, group_name=new_title, admin_list=admin_list)


@router.my_chat_member(F.new_chat_member.status.in_({ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}))
async def bot_removed(event: ChatMemberUpdated) -> None:
    chat = event.chat