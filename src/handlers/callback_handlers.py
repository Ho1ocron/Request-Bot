from aiogram import Router
from aiogram import F, Router, types


router = Router(name=__name__)


@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str("Your number is 1"))                      