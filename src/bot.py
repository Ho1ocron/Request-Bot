from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asyncio import run
import handlers, logging, sys
from settings import TOKEN
from database.actions import init_db, close_db


async def main() -> None:
    
    bot = Bot(
        TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    
    dp.include_routers(
        handlers.message_router,
        handlers.callback_router,
        handlers.admin_router,
        handlers.group_message_router
    )

    await init_db()
    await dp.start_polling(bot)
    print("working")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run((main()))


    
