from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#def create_keyboard(text: str, callback_data: Optional[str] = None, url: Optional[str] = None) -> InlineKeyboardBuilder:
#    builder = InlineKeyboardBuilder()
#    builder.add(InlineKeyboardButton(text=text, callback_data=callback_data, url=url))
#    return builder


#def create_keyboard(*args: InlineKeyboardButton) -> InlineKeyboardBuilder:
#    return InlineKeyboardBuilder().add(*args)


def main_keyboard() -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="📎 Add to your group", url="https://t.me/ilovethissomuchbot?startgroup=true")
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