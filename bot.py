import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.bot_routers import router


load_dotenv()
bot_api_token = os.getenv('BOT_API_TOKEN')

bot = Bot(bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('bot start')
        asyncio.run(start_bot())
    except (KeyboardInterrupt, RuntimeError):
        print("bot was terminated")
