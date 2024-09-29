import asyncio

#импорт нужных модулей для работы бота
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

#создание бота по токену
bot = Bot(token = TOKEN)
dp = Dispatcher()

#ответ после нажатия /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer("Бот запущен!")

#ответ после нажатия /info
@dp.message(Command("info"))
async def get_info(message: Message):
    await message.answer("Добро пожаловать в бот Fluffy trail, который был создан для помощи бездомным животным! \n"
                         "Здесь вы можете узнать ближайшее местонахождение зверюшек, чтобы прийти и покормить их или забрать к себе \n"
                         "Также есть возможность добавлять новые точки, где находятся нуждающиеся животные")

#главная функция, отправляющая запрос на сервер тг
async def main():
    await dp.start_polling(bot)

#запуск главной функции
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")