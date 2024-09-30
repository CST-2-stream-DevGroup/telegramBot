from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import app.keyboards as kb

router = Router()

#ответ после нажатия /start
@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer_photo(photo='AgACAgIAAxkBAANNZvlurmgJ3j-za2LmkPDn0diBGhUAAkrhMRvH79FL8-Q1NacBlQYBAAMCAAN4AAM2BA',
                               caption='Привет! Я бот, созданный для помощи бездомным животным. '
                                       'С моей помощью ты можешь отмечать на карте места, где видишь животных, '
                                       'нуждающихся в еде и заботе. Благодаря этому другие люди смогут прийти и помочь им.\n\n'
                                       'Чтобы начать, используй команды:\n'
                                       '/add_location — отметить новое место.\n'
                                       '/view_map — посмотреть карту с отмеченными животными.\n'
                                       '/info — узнать больше о том, как я работаю.\n\n'
                                       'Спасибо, что помогаешь друзьям нашим меньшим!',
                               reply_markup=kb.main)

#ответ после /info
@router.message(Command("info"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в бот Fluffy trail, который был создан для помощи бездомным животным \n"
                         "Здесь вы можете узнать ближайшее местонахождение зверюшек \n"
                         "Также есть возможность добавлять новые точки, где находятся нуждающиеся животные")

#загрузка фото в сам бот, чтобы можно было их потом использовать
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')
