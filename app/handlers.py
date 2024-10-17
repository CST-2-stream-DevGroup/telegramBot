from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import telegramBot.app.db as db1
import telegramBot.app.keyboards as kb
from telegramBot.app.db import db_start, take_coords
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from math import sin, cos, sqrt, atan2, radians
from aiogram import Bot
from telegramBot.config import TOKEN

bot1 = Bot(token=TOKEN)


def rast(lat1, lon1, lat2, lon2):
    radius = 6371  # km
    dlat = radians(float(lat2) - float(lat1))
    dlon = radians(float(lon2) - (lon1))
    a = (sin(dlat / 2) * sin(dlat / 2) +
         cos(radians(float(lat1))) * cos(radians(float(lat2))) *
         sin(dlon / 2) * sin(dlon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c
    return d


class Geo(StatesGroup):
    get_coor = State()
    pr_coor = State()
    pic = State()
    tex = State()


router = Router()


# ответ после нажатия /start

async def on_startup():
    await db_start()


@router.message(F.text == "Посмотреть карту")
async def send_location2(message: Message, state: FSMContext):
    await state.set_state(Geo.pr_coor)
    await message.reply("Отправь свои координаты!", reply_markup=kb.my_loc)


@router.message(Geo.pr_coor, F.location)
async def user_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(f"Ваши координаты {lat}, {lon}",
                         reply_markup=kb.main)
    # array from the database
    bd = await take_coords()

    # nearest points
    m = [0] * 3
    m[0] = 10000000000
    coordt1 = [0] * 2
    coordt2 = [0] * 2
    coordt3 = [0] * 2

    # database search
    for i in range(len(bd)):
        t = rast(lat, lon, bd[i][0], bd[i][1])
        if t < m[0]:
            m[2] = m[1]
            m[1] = m[0]
            m[0] = t
            coordt1[0], coordt1[1] = bd[i][0], bd[i][1]
            coordt2[0], coordt2[1] = coordt1[0], coordt1[1]
            coordt3[0], coordt3[1] = coordt2[0], coordt2[1]
        elif t < m[1]:
            m[2] = m[1]
            m[1] = t
            coordt2[0], coordt2[1] = bd[i][0], bd[i][1]
            coordt3[0], coordt3[1] = coordt2[0], coordt2[1]
        elif t < m[2]:
            m[2] = t
            coordt3[0], coordt3[1] = bd[i][0], bd[i][1]
    await state.clear()

    # print
    if m[0] > 1000:  # если животных нет в радиусе 1000км
        await message.answer("Рядом с вами нет бездомных животных")
    elif (m[1] > 1000) or (coordt2 == coordt1):  # если 1 животное в радиусе 1000км
        await message.answer("Рядом с вами только одно животное")
        await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1])
    elif (m[2] > 1000) or (coordt3 == coordt2):  # если 2 животных в радиусе 1000км
        await message.answer("Вот геолокации ближайших к вам бездомных животных")
        await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1])
        await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1])
    else:  # если 3 животных в радиусе 1000км
        await message.answer("Вот геолокации ближайших к вам бездомных животных")
        await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1])
        await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1])
        await bot1.send_location(message.from_user.id, coordt3[0], coordt3[1])


@router.message(F.text == "Добавить метку")
async def send_location2(message: Message, state: FSMContext):
    await state.set_state(Geo.get_coor)
    await message.reply("Отправь свои координаты!", reply_markup=kb.my_loc)


@router.message(Geo.get_coor, F.location)
async def handle_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    b = str(message.from_user.id) + " " + str(lat) + " " + str(lon)
    await state.update_data(get_coor=b)
    await message.reply("Прикрепи фото! (Или напиши 'нет')")
    await state.set_state(Geo.pic)


# прикрепляем фото
@router.message(Geo.pic, F.text)
async def send_photo1(message: Message, state: FSMContext):
    if (message.text == 'нет') or (message.text == 'Нет'):
        await state.update_data(pic='нет')
        await message.reply("Фото не добавлено")
        await message.reply("Отправь описание или напиши 'нет'")
        await state.set_state(Geo.tex)
    else:
        await state.clear()
        await message.reply("Попробуй заново добавить координаты",
                            reply_markup=kb.main)


@router.message(Geo.pic, F.photo)
async def send_photo2(message: Message, state: FSMContext):
    ph = message.photo[-1].file_id
    await state.update_data(pic=ph)
    await state.set_state(Geo.tex)


# прикрепляем описание
@router.message(Geo.tex, F.text)
async def send_text(message: Message, state: FSMContext):
    if (message.text == 'нет') or (message.text == 'Нет'):
        await state.update_data(tex='нет')
        await message.reply("Описание не добавлено",
                            reply_markup=kb.main)
        # вот тут напишешь свою базу данных
        await state.clear()
    else:
        await state.clear()
        await message.reply("Описание добавлено",
                            reply_markup=kb.main)
        await state.update_data(tex=message.text)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAANNZvlurmgJ3j-za2LmkPDn0diBGhUAAkrhMRvH79FL8-Q1NacBlQYBAAMCAAN4AAM2BA',
        caption='Привет! Я бот, созданный для помощи бездомным животным. '
                'С моей помощью ты можешь отмечать на карте места, где видишь животных, '
                'нуждающихся в еде и заботе. Благодаря этому другие люди смогут прийти и помочь им.\n\n'
                'Чтобы начать, используй команды:\n'
                '/add_location — отметить новое место.\n'
                '/view_map — посмотреть карту с отмеченными животными.\n'
                '/info — узнать больше о том, как я работаю.\n\n'
                'Спасибо, что помогаешь друзьям нашим меньшим!'
                '/support - для отправления обращения в поддержку, если возникнут проблемы',
        reply_markup=kb.main)


# ответ после /info
@router.message(Command("info"))
async def cmd_start(message: Message):
    await db_start()
    await message.answer("Добро пожаловать в бот Fluffy trail, который был создан для помощи бездомным животным \n"
                         "Здесь вы можете узнать ближайшее местонахождение зверюшек \n"
                         "Также есть возможность добавлять новые точки, где находятся нуждающиеся животные")


# загрузка фото в сам бот, чтобы можно было их потом использовать
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')


# Отправление сообщения админу
@router.message(Command("get_support"))
async def cmd_start(message: Message):
    await db_start()
    await message.bot.forward_message(chat_id="914902185", from_chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Ваш ответ принят! Поддержка рассмотрит его в течение суток.")


# Команда /support для получения инфы по поводу отправки запроса
@router.message(Command("support"))
async def cmd_start(message: Message):
    await db_start()
    await message.answer(
        "Напишите /get_support и опишите проблему в этом же сообщении. После чего оно будет перенаправлено в поддержку")