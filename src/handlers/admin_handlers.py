from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from settings import ADMIN_IDS


router = Router(name=__name__)

router.message.filter(
    F.from_user.id.in_(ADMIN_IDS),
)


@router.message(Command(commands=['admin']))
async def admin(message: Message) -> None:
    await message.answer('admin')