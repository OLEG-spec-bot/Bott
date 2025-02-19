import asyncio

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router


bot = Bot(token=BOT_TOKEN)

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")