from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from settings import ADMIN_IDS
from database.actions import close_db, init_db


router = Router(name=__name__)

router.message.filter(
    F.from_user.id.in_(ADMIN_IDS),
)


@router.message(Command(commands=['admin']))
async def admin(message: Message) -> None:
    await message.answer('admin')


@router.message(Command(commands=["close"]))
async def closeDB(message: Message) -> None:
    await close_db()
    await message.answer("Database closed.")



@router.message(Command(commands=["init"]))
async def initDB(message: Message) -> None:
    await init_db()
    await message.answer("Database inited.")


@router.message(Command("status"))
async def check_fsm_state(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await message.answer(f"Your current FSM state is: {current_state}")