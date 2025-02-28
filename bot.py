import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiohttp import web
from config import BOT_TOKEN
from handlers import router

bot = Bot(token=BOT_TOKEN)

async def on_start(request):
    # Получаем данные из запроса
    data = await request.json()
    update = types.Update(**data)
    # Обрабатываем обновления
    await bot.process_new_updates([update])
    return web.Response()

async def set_webhook():
    # URL для webhook на Render
    webhook_url = "https://<your-render-url>.onrender.com/webhook"  # Замените на ваш URL
    # Устанавливаем webhook
    await bot.set_webhook(webhook_url)
    print(f"Webhook установлен на {webhook_url}")

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    
    # Устанавливаем webhook
    await set_webhook()

    # Настроим aiohttp для обработки webhook запросов
    app = web.Application()
    app.router.add_post('/webhook', on_start)  # Обработка запросов от Telegram на /webhook
    print("Webhook сервер работает...")

    # Используем порт, предоставленный Render через переменную окружения
    port = int(os.environ.get('PORT', 8080))  # Порт, предоставленный Render (по умолчанию 8080)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)  # Слушаем на порту, предоставленном Render
    await site.start()

    # Ожидаем до остановки
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

