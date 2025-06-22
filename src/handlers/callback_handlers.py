from aiogram import F, Router
from aiogram.types import CallbackQuery
from database.actions import create_group, get_user
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaAnimation, InputMediaDocument, InputMediaPhoto, InputMediaVideo 
from states import PostStates, GroupCallback, bot_state
from typing import List
import asyncio


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


@router.callback_query(F.data == "custom_link")
async def create_link(callback: CallbackQuery) -> None:
    await callback.message.answer(
        (
            "📝 Send me a sentence you want to use in your link"
        )
    )


@router.callback_query(F.data == "group_continue")
async def group_continue(callback: CallbackQuery) -> None:
    await create_group()
    await callback.message.answer(
        (
            "Alright, here we go!\n\n"
        )
    )


@router.callback_query(F.data == "cancel", PostStates.waiting_for_post,)
async def Cancel_sending(callback: CallbackQuery, state: FSMContext) -> None: 
    await callback.message.answer(
        (
            "Sending cancelled."
        )
    )
    bot_state.set_message_to_forward(None)  # Clear the message to forward
    bot_state.set_media_group_messages(None) # Clear the media group messages


@router.callback_query(GroupCallback.filter())
async def forwarding(callback: CallbackQuery, callback_data: GroupCallback):
    await callback.answer(f"{callback_data.group_name=}")


user_timers = {int: asyncio.Task}
async def timer_action(callback: CallbackQuery, seconds: int, user_id: int) -> None:
    try:
        await asyncio.sleep(seconds)  # Timer duration
        bot_state.set_message_to_forward(None)  # Clear the message to forward
        bot_state.set_media_group_messages(None)  # Clear the media group messages
    except asyncio.CancelledError:
        return


@router.callback_query(F.data.startswith("select_group:"))
async def select_group(callback: CallbackQuery, state: FSMContext) -> None:
    group_id = callback.data.split(":")[1]
    # Here you would typically handle the selection of the group, e.g., store it in the database or state
    # For now, we just acknowledge the selection
    # await callback.answer(f"Selected group ID: {group_id}")
    # Retrieve the message_id to forward from FSM state
    # message_id = data.get("message_id_to_forward")
    message = bot_state.get_message_to_forward()
    media_group = bot_state.get_media_group_messages()
    media_group.sort(key=lambda x: x.message_id)  # Sort media group by message_id
    user_id = callback.message.chat.id
    user = await get_user(user_id=user_id)
    extr_caption = f'\n\n<a href="tg://user?id={user_id}">{user.name}</a>'
    if not message and not media_group:
        await callback.message.answer("No message to send found.")
        return
    # Forward the message to the selected group
    if not media_group:
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
        await callback.message.answer("Your post sent successfully.")
        # asyncio.create_task(start_timer(callback=callback, seconds=10, user_id=user_id))
        if user_id in user_timers:
            user_timers[user_id].cancel()
        task = asyncio.create_task(timer_action(callback=callback, seconds=20, user_id=user_id))
        user_timers[user_id] = task
        return
    _media_group = []
    user_id = callback.message.chat.id
    user = await get_user(user_id=user_id)
    extr_caption = f'\n\n<a href="tg://user?id={user_id}">{user.name}</a>'
    max_len_caption = max(media_group, key=lambda x: len(x.caption) if x.caption else 0).caption
    for idx, msg in enumerate(media_group):
        caption = msg.caption if msg.caption is not None else None # Only the first message in the media group should have a caption and I should fix it so there is always captions
        if caption == max_len_caption and caption != None:
            caption += extr_caption
        else:
            if idx == 0:
                caption = extr_caption
        if msg.photo: # Пофиксить чтобы фотки были в правильном порядке, а не в рандомном через insert() если есть подпись.
            # Эта часть кода должна быть исправлена, чтобы использовать правильный порядок фотографий через .sort() по id
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
            # _media_group[0].caption = _media_group[0].caption + extr_caption if _media_group[0].caption else extr_caption
            await callback.bot.send_media_group(
                chat_id=group_id,
                media=_media_group
            )
            await callback.message.answer("Your post sent successfully.")
    except Exception as e:
        await callback.message.answer(f"Error occurred while sending media group: {e}")
    finally:
        if user_id in user_timers:
            user_timers[user_id].cancel()
        task = asyncio.create_task(timer_action(callback=callback, seconds=20, user_id=user_id))
        user_timers[user_id] = task
    #     asyncio.create_task(start_timer(callback=callback, seconds=10, user_id=user_id))  # Start a timer for 10 seconds
        # set_message_to_forward(None)  # Clear the message to forward
        # save_media_group_messages(None)  # Clear the media group messages

# id to add: Add source from which the message was sent, so that it can be used in the caption.

