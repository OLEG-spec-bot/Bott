import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from config import BOT_TOKEN
from handlers import router

bot = Bot(token=BOT_TOKEN)

async def on_start(request):
    return web.Response(text="Server is running")

async def on_shutdown(app):
    await bot.session.close()

async def main():
    # Создание диспетчера и подключение роутера
    dp = Dispatcher()
    dp.include_router(router)
    
    # Создание приложения aiohttp
    app = web.Application()
    app.add_routes([web.get('/', on_start)])

    # Устанавливаем вебхук
    webhook_url = 'https://Bott.onrender.com'
'
    await bot.set_webhook(webhook_url)

    # Запуск веб-сервера на порту 8000
    app.on_shutdown.append(on_shutdown)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)  # Веб-сервер будет слушать порт 8000
    await site.start()

    print("Server is running...")

    # Это будет ждать пока не произойдёт исключение, например, при остановке приложения
    try:
        while True:
            await asyncio.sleep(3600)  # Это просто, чтобы не завершать программу сразу
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

