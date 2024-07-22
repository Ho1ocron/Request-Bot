import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import handlers
import logging
from settings import TOKEN
import sys


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
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())