import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from config import BOT_TOKEN
from handlers import router
from aiogram.webhook.aiohttp import send_webhook

# Создаем объект бота с переданным токеном
bot = Bot(token=BOT_TOKEN)

async def on_start():
    dp = Dispatcher(bot)

    # Подключаем роутер
    dp.include_router(router)

    # Устанавливаем webhook URL (в зависимости от вашего домена на Render)
    webhook_url = "https://Bott.onrender.com/{BOT_TOKEN}"

    # Настроим webhook
    await bot.set_webhook(webhook_url)

    print(f"Webhook установлен на {webhook_url}")

    # Webhook-обработчик
    await send_webhook(bot)

if __name__ == '__main__':
    try:
        asyncio.run(on_start())
    except KeyboardInterrupt:
        print("Бот остановлен")
