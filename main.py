# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.handlers import router
from bot.config import TELEGRAM_TOKEN  # ← Только эту переменную мы теперь импортируем


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())