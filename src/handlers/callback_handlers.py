from aiogram import F, Router, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import(
    CallbackQuery,
    InputMediaDocument, 
    InputMediaPhoto, 
    InputMediaVideo ,
    Message,
    InlineKeyboardMarkup
) 

from database import get_user, get_group
from utils import (
    get_message_to_forward, 
    get_media_group_to_forward,
    delete_saved_message,
)


router = Router(name=__name__)


@router.callback_query(F.data == "send_command_list")
async def send_random_value(callback: CallbackQuery) -> None:
    await callback.message.answer(
        (
            "No commands here yet"
            ""
            ""
        )
    )



@router.callback_query(F.data == "cancel")
async def Cancel_sending(callback: CallbackQuery) -> None: 
    await callback.message.answer(
        (
            "Sending cancelled."
        )
    )
    await delete_saved_message(key=f"message:{callback.from_user.id}")



@router.callback_query(F.data.startswith("select_group:"))
async def select_group(callback: CallbackQuery, state: FSMContext) -> None:
    group_id = callback.data.split(":")[1]
    message_type = callback.data.split(":")[2]

    message: Message | None = None
    media_group: list | None = None

    group = await get_group(group_id)
    
    if message_type == "media_group":
        media_group = await get_media_group_to_forward(key=f"message:{callback.from_user.id}")
        media_group.sort(key=lambda x: x.message_id)
    elif message_type == "message":
        message = await get_message_to_forward(key=f"message:{callback.from_user.id}")

    user_id = callback.message.chat.id
    user = await get_user(user_id=user_id)
    extr_caption = f'\n\n<a href="tg://user?id={user_id}">{user.name}</a>'

    if not message and not media_group:
        await callback.message.answer("No message to send found.")
        await delete_saved_message(key=f"message:{callback.from_user.id}")
        return
    
    # No we need to remove the button that user pressed so they won't send their post multiple times to one channel
    message_markup = callback.message.reply_markup
    new_keyboard = []

    # In this loop we find the button that user pressed and build remove it in the new keyboard
    new_keyboard = []
    for row in message_markup.inline_keyboard:
        new_row = [b for b in row if b.callback_data != callback.data]
        if new_row:  # Avoid empty rows
            new_keyboard.append(new_row)
    
    # Creating a new markup to replace the existing one
    new_markup = InlineKeyboardMarkup(inline_keyboard=new_keyboard)

    # Forward the message to the selected group
    if message_type == "message":
        message_text = message.caption or message.text or ""
        message_text += extr_caption
        # Get the original message
        if message.text:
            await callback.bot.send_message(
                chat_id=group_id,
                text=message_text,
            )
        elif message.photo:
            await callback.bot.send_photo(
                chat_id=group_id,
                photo=message.photo[-1].file_id,
                caption=message_text,
            )
        elif message.video:
            await callback.bot.send_video(
                chat_id=group_id,
                video=message.video.file_id,
                caption=message_text,
            )
        elif message.document:
            await callback.bot.send_document(
                chat_id=group_id,
                document=message.document.file_id,
                caption=message_text,
            )
        elif message.animation:
            await callback.bot.send_animation(
                chat_id=group_id,
                animation=message.animation.file_id,
                caption=message_text,
            )
        await callback.message.edit_reply_markup(reply_markup=new_markup)
        await callback.message.answer(f"Your post sent successfully to <b>{group.name}</b>!")
        return
    
    _media_group = []
    user_id = callback.message.chat.id
    user = await get_user(user_id=user_id)
    extr_caption = f'\n\n<a href="tg://user?id={user_id}">{user.name}</a>'
    max_len_caption = max(media_group, key=lambda x: len(x.caption) if x.caption else 0).caption
    idx: int
    msg: Message
    for idx, msg in enumerate(media_group):
        caption = msg.caption if msg.caption is not None else None # Only the first message in the media group should have a caption and I should fix it so there is always captions
        if caption == max_len_caption and caption != None:
            caption += extr_caption
        else:
            if idx == 0:
                caption = extr_caption
        if msg.photo: # Пофиксить чтобы фотки были в правильном порядке, а не в рандомном через insert() если есть подпись.
            file_id = msg.photo[-1].file_id
            _media_group.append(InputMediaPhoto(media=file_id, caption=caption))
        elif msg.video:
            file_id = msg.video.file_id
            _media_group.append(InputMediaVideo(media=file_id, caption=caption))
        elif msg.document:
            file_id = msg.document.file_id
            _media_group.append(InputMediaDocument(media=file_id, caption=caption))
        # elif msg.animation:
        #     file_id = msg.animation.file_id
        #     _media_group.append(InputMediaAnimation(media=file_id, caption=caption))
    try:
        if _media_group:
            await callback.bot.send_media_group(
                chat_id=group_id,
                media=_media_group
            )
            await callback.message.edit_reply_markup(reply_markup=new_markup)
            await callback.message.answer(f"Your post sent successfully to <b>{group.name}</b>!")
    except Exception as e:
        await callback.message.answer(f"Error occurred while sending media group: {e}")

# id to add: Add source from which the message was sent, so that it can be used in the caption.