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
from src.database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

async def on_startup(dispatcher: Dispatcher):
    # Initialize database tables on startup
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("ZenithID Bot: Database synced and service started.")

async def on_shutdown(dispatcher: Dispatcher):
    print("ZenithID Bot: Shutting down.")

async def main():
    # Performance optimization using uvloop
    uvloop.install()

    # Redis initialization for FSM storage
    redis = Redis.from_url(settings.REDIS_URL)
    storage = RedisStorage(redis=redis)

    # Bot client initialization
    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    # Middleware and Router registration
    dp.update.outer_middleware(UserMiddleware())
    dp.include_router(main_router)

    # Register lifecycle hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await redis.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")