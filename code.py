import asyncio

#импорт нужных модулей для работы бота
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router

#создание бота по токену
bot = Bot(token = TOKEN)
dp = Dispatcher()

#главная функция, отправляющая запрос на сервер тг
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

#запуск главной функции
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
