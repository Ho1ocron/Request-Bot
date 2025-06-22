from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from settings import ADMIN_IDS
from database.actions import close_db, init_db
from states import bot_state
import asyncio


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


@router.message(Command(commands=["clear_state"]))
async def clear_state(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("✅ Your state has been cleared.")
    bot_state.set_message_to_forward(None)
    bot_state.set_media_group_messages(None)


async def timer_action(user_id: int, chat_id: int, message: Message) -> None:
    try:
        await asyncio.sleep(10)  # Timer duration
        await message.bot.send_message(chat_id, f"⏰ User {user_id}, timer finished!")
    except asyncio.CancelledError:
        # Timer was reset/cancelled
        print(f"Timer for user {user_id} was cancelled.")
        return


user_timers = {}
@router.message(Command(commands=["timer"]))
async def start_timer(message: Message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Cancel existing timer if running
    if user_id in user_timers:
        user_timers[user_id].cancel()

    # Create and store a new timer task
    task = asyncio.create_task(timer_action(user_id, chat_id, message))
    user_timers[user_id] = task

    await message.reply("⏳ Timer started/reset! I’ll remind you in 10 seconds if you don’t touch it again.")
