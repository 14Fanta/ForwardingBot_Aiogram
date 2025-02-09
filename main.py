import asyncio
from dotenv import load_dotenv
import logging

from app.database.models import async_main
from app.handlers import bot,dp,user_router

async def main():
    load_dotenv()
    await async_main()
    dp.include_router(user_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turned off...")