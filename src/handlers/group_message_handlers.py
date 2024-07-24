from aiogram import Router, F
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.types import Message


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
    
    await message.answer('bot added to group')
