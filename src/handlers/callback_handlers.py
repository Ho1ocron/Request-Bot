from aiogram import F, Router
from aiogram.types import CallbackQuery
from database.actions import create_group
from aiogram.fsm.context import FSMContext
from states import PostStates, GroupCallback 


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
    await state.clear()
    await callback.message.answer(
        (
            "Action cancelled."
        )
    )
    await state.set_state(PostStates.waiting_for_post)


@router.callback_query(GroupCallback.filter())
async def forwarding(callback: CallbackQuery, callback_data: GroupCallback):
    await callback.answer(f"{callback_data.group_name=}")