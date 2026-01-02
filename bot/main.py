import asyncio
from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.database.db import init_db
from bot.handlers import start, expense, income, stats, zero, cancel, notes


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(expense.router)
    dp.include_router(income.router)
    dp.include_router(stats.router)
    dp.include_router(zero.router)
    dp.include_router(cancel.router)
    dp.include_router(notes.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())
