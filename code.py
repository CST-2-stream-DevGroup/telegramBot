import asyncio

#импорт нужных модулей для работы бота
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

#создание бота по токену
bot = Bot(token = TOKEN)
dp = Dispatcher()

#ответ после нажатия /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer("Бот запущен!")

#главная функция, отправляющая запрос на сервер тг
async def main():
    await dp.start_polling(bot)

#запуск главной функции
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")