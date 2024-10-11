from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import telegramBot.app.db as db1
import telegramBot.app.keyboards as kb
from telegramBot.app.db import db_start, take_coords
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from math import sin, cos, sqrt, atan2, radians

def rast(lat1, lon1, lat2, lon2):
    radius = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat / 2) * sin(dlat / 2) +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon / 2) * sin(dlon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c
    return d

class Geo(StatesGroup):
    get_coor = State()
    pr_coor = State()

router = Router()

#ответ после нажатия /start

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
    #array from the datebase
    bd = await take_coords()

    #nearest points
    m = [0] * 3
    m[0] = 10000000000
    coordt1 = [0] * 2
    coordt2 = [0] * 2
    coordt3 = [0] * 2

    #database search
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

    #print
    if m[0] > 1000:  # если животных нет в радиусе 1000км
        await message.answer("Рядом с Вами нет бездомных животных")
    elif (m[1] > 1000) or (coordt2 == coordt1):  # если 1 животное в радиусе 1000км
        await message.answer(f'Ближайшее животное находится на расстоянии {m[0]} километров от Вас!\
                \n 1) широта: {coordt1[0]} долгота: {coordt1[1]}')
    elif (m[2] > 1000) or (coordt3 == coordt2):  # если 2 животных в радиусе 1000км
        await message.answer(f'Ближайшие животныи находятся на расстоянии {m[0]} километров, {m[1]} километров от Вас!\
                \n 1) широта: {coordt1[0]} долгота: {coordt1[1]} \
                \n 2) широта: {coordt2[0]} долгота: {coordt2[1]}')
    else:  # если 3 животных в радиусе 1000км
        await message.answer(f'Ближайшие животныи находятся на расстоянии {m[0]} километров, {m[1]} километров, {m[2]} километров от Вас!\
              \n 1) широта: {coordt1[0]} долгота: {coordt1[1]} \
              \n 2) широта: {coordt2[0]} долгота: {coordt2[1]} \
              \n 3) широта: {coordt3[0]} долгота: {coordt3[1]}')

@router.message(F.text == "Добавить метку")
async def send_location2(message: Message, state: FSMContext):
    await state.set_state(Geo.get_coor)
    await message.reply("Отправь свои координаты!", reply_markup=kb.my_loc)

@router.message(Geo.get_coor, F.location)
async def handle_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer("Ваши координаты добавлены в бд",
                               reply_markup=kb.main)
    await db1.create(user_id=message.from_user.id, lat=lat, long=lon)
    await state.clear()

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
    await db_start()
    await message.answer("Добро пожаловать в бот Fluffy trail, который был создан для помощи бездомным животным \n"
                         "Здесь вы можете узнать ближайшее местонахождение зверюшек \n"
                         "Также есть возможность добавлять новые точки, где находятся нуждающиеся животные")

#загрузка фото в сам бот, чтобы можно было их потом использовать
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')
