from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asyncio import run
import handlers, logging, sys
import handlers.message_handlers
from settings import TOKEN, ADMIN_IDS
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
    handlers.message_handlers.bot_name = await bot.get_me()
    await init_db()
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run((main()))