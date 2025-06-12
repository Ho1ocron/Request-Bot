from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states import GroupCallback
from database.actions import get_group
from asyncio import run


#def create_keyboard(text: str, callback_data: Optional[str] = None, url: Optional[str] = None) -> InlineKeyboardBuilder:
#    builder = InlineKeyboardBuilder()
#    builder.add(InlineKeyboardButton(text=text, callback_data=callback_data, url=url))
#    return builder


#def create_keyboard(*args: InlineKeyboardButton) -> InlineKeyboardBuilder:
#    return InlineKeyboardBuilder().add(*args)


def main_keyboard(bot_name: str) -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="📎 Add to your group", url=f"https://t.me/{bot_name}?startgroup=true")
    )


def user_help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="📝 Command List", callback_data="send_command_list"),
                InlineKeyboardButton(text="📌 FAQ", callback_data="send_faq"),
            ],
            [
                InlineKeyboardButton(text="🔍 About Us", callback_data="send_about_us"),
            ],
        ]
    )


def group_link_keyboard() -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="📌Generate your custom link", callback_data="custom_link")
    )


def group_continue_keyboard() -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="Continue ▶️", callback_data="group_continue")
    )


async def choose_channel(groups:list[int]) -> InlineKeyboardMarkup:
    keyboard = []
    cancelbtn = [InlineKeyboardButton(text="Cancel", callback_data="cancel")]
    for _id in groups:
            
        group = await get_group(group_id=_id)
        print(type(group))
        keyboard.append(
            InlineKeyboardButton(text=group.name, callback_data=GroupCallback(gropu_id=_id, group_name=group.name).pack())
        )
    return InlineKeyboardMarkup(inline_keyboard=[keyboard, cancelbtn])