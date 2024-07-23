from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link


router = Router(name=__name__)


@router.message(Command(commands=['start', 'help']))
async def start(message: Message) -> None:
    await message.answer('start')
