import asyncio
import uvloop
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis
from config.settings import settings
from src.bot.handlers import router as main_router
from src.bot.middlewares import UserMiddleware

async def on_startup(dispatcher: Dispatcher):
    print("ZenithID Bot started successfully.")

async def on_shutdown(dispatcher: Dispatcher):
    print("ZenithID Bot shut down gracefully.")

async def main():
    # Use uvloop for better performance
    uvloop.install()

    # Initialize Redis storage for FSM
    redis = Redis.from_url(settings.REDIS_URL)
    storage = RedisStorage(redis=redis)

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    # Register middleware
    dp.update.outer_middleware(UserMiddleware())

    # Include routers
    dp.include_router(main_router)

    # Register startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await redis.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")