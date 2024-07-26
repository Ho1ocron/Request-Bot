from aiogram import F, Router
from aiogram.types import CallbackQuery


router = Router(name=__name__)

# callback.bot | message.bot

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery) -> None:
    await callback.message.answer(str("Your number is 1"))
