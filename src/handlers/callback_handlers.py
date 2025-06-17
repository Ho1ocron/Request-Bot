from aiogram import F, Router
from aiogram.types import CallbackQuery
from database.actions import create_group
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaAnimation, InputMediaDocument, InputMediaPhoto, InputMediaVideo 
from states import PostStates, GroupCallback, get_message_to_forward, set_message_to_forward, get_media_group_messages, save_media_group_messages



router = Router(name=__name__)

# callback.bot | message.bot

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
    set_message_to_forward(None)  # Clear the message to forward
    save_media_group_messages(None) # Clear the media group messages
    await state.clear()
    await state.set_state(PostStates.waiting_for_post)


@router.callback_query(GroupCallback.filter())
async def forwarding(callback: CallbackQuery, callback_data: GroupCallback):
    await callback.answer(f"{callback_data.group_name=}")


@router.callback_query(F.data.startswith("select_group:"))
async def select_group(callback: CallbackQuery, state: FSMContext) -> None:
    group_id = callback.data.split(":")[1]
    print(f"Selected group ID: {group_id}")
    # Here you would typically handle the selection of the group, e.g., store it in the database or state
    # For now, we just acknowledge the selection
    # await callback.answer(f"Selected group ID: {group_id}")
    
    # Optionally, you can send a confirmation message to the user
    # await callback.message.answer(
    #     f"You have selected the group with ID: {group_id}"
    # )
    # Import the FSM state where the message_id is s`tored

    # Get FSMContext for this user

    # Retrieve the message_id to forward from FSM state
    data = await state.get_data()
    message_id = data.get("message_id_to_forward")
    message_id = get_message_to_forward()[0]
    to_hide_name = get_message_to_forward()[1]
    media_group = get_media_group_messages()
    if not message_id and not media_group:
        await callback.message.answer("No message to send found.")
        return
    to_hide_name = True
    # Forward the message to the selected group
    if not media_group:
        # Get the original message
        await callback.bot.copy_message(
            chat_id=group_id,
            from_chat_id=callback.message.chat.id,
            message_id=message_id
        )
        # Copy the text without sender info
        # await callback.bot.send_message(
        #     chat_id=group_id,
        #     text=original_message.text or "",
        #     entities=original_message.entities
        # )
        await callback.message.answer("Your post sent successfully.")
        set_message_to_forward(None)  # Clear the message to forward
        await state.clear()
        await state.set_state(PostStates.waiting_for_post)
        print(message_id, group_id)
        return
    # copied_ids = []
    # for media in media_group:
    #     copied = await callback.bot.copy_message(
    #         chat_id=group_id,
    #         from_chat_id=media.chat.id,
    #         message_id=media.message_id
    #     )
    #     copied_ids.append(copied.message_id)
    _media_group = []
    for idx, msg in enumerate(media_group):
        caption = msg.caption if idx == 0 else None # Only the first message in the media group should have a caption and I should fix it so there is always captions
        if msg.photo:
            file_id = msg.photo[-1].file_id
            _media_group.append(InputMediaPhoto(media=file_id, caption=caption))
        elif msg.video:
            file_id = msg.video.file_id
            _media_group.append(InputMediaVideo(media=file_id, caption=caption))
        elif msg.document:
            file_id = msg.document.file_id
            _media_group.append(InputMediaDocument(media=file_id, caption=caption))
        elif msg.animation:
            file_id = msg.animation.file_id
            _media_group.append(InputMediaAnimation(media=file_id, caption=caption))

    if _media_group:
        await callback.bot.send_media_group(
            chat_id=group_id,
            media=_media_group
        )
    set_message_to_forward(None)  # Clear the message to forward
    save_media_group_messages(None)  # Clear the media group messages
    await callback.message.answer("Your post sent successfully.")
    await state.clear()
    await state.set_state(PostStates.waiting_for_post)
