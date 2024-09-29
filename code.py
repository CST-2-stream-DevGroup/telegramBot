import asyncio

#импорт нужных модулей для работы бота
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

#создание бота по токену
bot = Bot(token = TOKEN)
dp = Dispatcher()

#ответ после нажатия /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer_photo(photo='AgACAgIAAxkBAAM0ZvlVMGSO3jDDIn8rSa5cthZxFswAAmjgMRvH79FL06g-JhlUG3cBAAMCAAN5AAM2BA',
                               caption='Привет! Я бот, созданный для помощи бездомным животным. '
                                       'С моей помощью ты можешь отмечать на карте места, где видишь животных, '
                                       'нуждающихся в еде и заботе. Благодаря этому другие люди смогут прийти и помочь им.\n\n'
                                       'Чтобы начать, используй команды:\n'
                                       '/add_location — отметить новое место.\n'
                                       '/view_map — посмотреть карту с отмеченными животными.\n'
                                       '/info — узнать больше о том, как я работаю.\n\n'
                                       'Спасибо, что помогаешь нашим меньшим друзьям!')

#загрузка фото в сам бот, чтобы можно было их потом использовать
@dp.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')

#главная функция, отправляющая запрос на сервер тг
async def main():
    await dp.start_polling(bot)

#запуск главной функции
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")