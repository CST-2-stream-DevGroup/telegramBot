from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import telegramBot.app.db as db1
import telegramBot.app.keyboards as kb
from telegramBot.app.db import db_start, take_coords, take_inf, check_coords
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
            coordt3[0], coordt3[1] = coordt2[0], coordt2[1]
            coordt2[0], coordt2[1] = coordt1[0], coordt1[1]
            coordt1[0], coordt1[1] = bd[i][0], bd[i][1]
        elif t < m[1]:
            m[2] = m[1]
            m[1] = t
            coordt3[0], coordt3[1] = coordt2[0], coordt2[1]
            coordt2[0], coordt2[1] = bd[i][0], bd[i][1]
        elif t < m[2]:
            m[2] = t
            coordt3[0], coordt3[1] = bd[i][0], bd[i][1]
    await state.clear()
    if m[0] > 1000:  # если животных нет в радиусе 1000км
        await message.answer("Рядом с вами нет бездомных животных")
    elif (m[1] > 1000) or (coordt2 == coordt1):  # если 1 животное в радиусе 1000км
        await message.answer("Рядом с вами только одно животное")
        data = await take_inf(lt=coordt1[0], ln=coordt1[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                              photo=f"{data[0][0]}",
                              caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id,f"Фото: не приложено \n"
                                                         f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)


    elif (m[2] > 1000) or (coordt3 == coordt2):  # если 2 животных в радиусе 1000км
        await message.answer("Вот геолокации ближайших к вам бездомных животных")

        data = await take_inf(lt=coordt1[0], ln=coordt1[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                                  photo=f'{data[0][0]}',
                                  caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id, f"Фото: не приложено \n"
                                                          f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)

        data = await take_inf(lt=coordt2[0], ln=coordt2[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                                  photo=f"{data[0][0]}",
                                  caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id, f"Фото: не приложено \n"
                                                          f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1], reply_markup=kb.main)
    else:  # если 3 животных в радиусе 1000км
        await message.answer("Вот геолокации ближайших к вам бездомных животных")

        data = await take_inf(lt=coordt1[0], ln=coordt1[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                                  photo=f"{data[0][0]}",
                                  caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id, f"Фото: не приложено \n"
                                                          f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt1[0], coordt1[1], reply_markup=kb.main)

        data = await take_inf(lt=coordt2[0], ln=coordt2[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                                  photo=f"{data[0][0]}",
                                  caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id, f"Фото: не приложено \n"
                                                          f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt2[0], coordt2[1], reply_markup=kb.main)

        data = await take_inf(lt=coordt3[0], ln=coordt3[1])
        is_photo = True if len(data[0][0]) >= 80 else False

        if (is_photo):
            await bot1.send_photo(message.from_user.id,
                                  photo=f"{data[0][0]}",
                                  caption=f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt3[0], coordt3[1], reply_markup=kb.main)
        else:
            await bot1.send_message(message.from_user.id, f"Фото: не приложено \n"
                                                          f"Описание: {data[0][1]}")
            await bot1.send_location(message.from_user.id, coordt3[0], coordt3[1], reply_markup=kb.main)


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
    if (message.text == "нет") or (message.text == "Нет"):
        await state.update_data(pic="нет")
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
    await message.reply("Отправь описание или напиши 'нет'")
    await state.set_state(Geo.tex)


# прикрепляем описание
@router.message(Geo.tex, F.text)
async def send_text(message: Message, state: FSMContext):
    data = await state.get_data()
    if_exists_coors_in_bd = await check_coords(data['get_coor'].split()[1], data['get_coor'].split()[2])
    if (message.text == "нет") or (message.text == "Нет"):
        if (if_exists_coors_in_bd):
            await db1.create(user_id=message.from_user.id, lat=data['get_coor'].split()[1],
                            long=data['get_coor'].split()[2], img=data['pic'], desc=message.text.lower())
            await message.reply("Новое место добавлено", reply_markup=kb.main)
        else:
            await message.reply("Это место уже есть в нашей базе данных", reply_markup=kb.main)
        await state.clear()
    else:
        if (if_exists_coors_in_bd):
            await db1.create(user_id=message.from_user.id, lat=data['get_coor'].split()[1],
                             long=data['get_coor'].split()[2], img=data['pic'], desc=message.text.lower())
            await message.reply("Новое место добавлено", reply_markup=kb.main)
        else:
            await message.reply("Это место уже есть в нашей базе данных", reply_markup=kb.main)
        await state.clear()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAANNZvlurmgJ3j-za2LmkPDn0diBGhUAAkrhMRvH79FL8-Q1NacBlQYBAAMCAAN4AAM2BA',
        caption="Привет! Я бот, созданный для помощи бездомным животным. "
                "С моей помощью ты можешь отмечать на карте места, где видишь бездомных животных, "
                "нуждающихся в еде и заботе. Благодаря этому другие люди смогут прийти и покормить их"
                " или забрать к себе.\n\n"
                "Для того, чтобы начать работу с ботом, используй кнопки на клавиатуре.\n\n"
                "Спасибо, что находишь время для помощи братьям нашим меньшим!\n"
                "Если возникнут проблемы при общении со мной, исопльзуйте комманду /support для "
                "получения помощи поддержки",
        reply_markup=kb.main)


# ответ после /info
@router.message(Command("info"))
async def cmd_start(message: Message):
    await db_start()
    await message.answer("Привет, друг! Мы очень рады, что ты хочешь сделать доброе дело! "
                         "Давай мы немного расскажем о работе нашего бота.\n\n"
                         "'Fluffy trail' был создан командой студентов, которые заинтересованы "
                         "в помощи животным, попавшим в беду. Принцип работы бота прост: "
                         "нажав несколько кнопок, ты можешь увидеть ближайшее к тебе "
                         "местонахождение животного, которое нуждается в помощи человека."
                         "Также, если ты встретил на улице зверюшек, ты можешь добавить их "
                         "геолокацию, если её ещё нет.\n\n "
                         "В боте существуют две основные кнопки: 'Добавить метку' и 'Посмотреть карту'\n."
                         "Нажав на первую, система попросит твои координаты и запомнит их. Далее "
                         "по возможности ты можешь отправить фотографию и описание, чтобы "
                         "по ним люди смогли узнать, какое это животное и в какая помощь еум нужна.\n"
                         "Нажав на вторую кнопку, бот также попросит твои координаты, затем "
                         "определит и отправит тебе ближайшую геолокацию зверька, которую "
                         "отметили другие люди, а также фотографию и описание, если они были сделаны.\n\n"
                         "Если у тебя возникнут проблемы с использованием бота или вопросы, не стесняйся "
                         "задавать их нам. Напиши команду /suppot и напиши то, о чём хочешь узнать. "
                         "В течение суток наша команда поможет тебе."
                         "Спасибо, что выбрали бот Fluffy trail!"

                         )


# загрузка фото в сам бот, чтобы можно было их потом использовать
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')


# Отправление сообщения админу
@router.message(Command("get_support"))
async def cmd_start(message: Message):
    await db_start()
    await message.bot.forward_message(chat_id="914902185", from_chat_id=message.chat.id,
                                      message_id=message.message_id)
    await message.answer("Ваш ответ принят! Поддержка рассмотрит его в течение суток.")


# Команда /support для получения инфы по поводу отправки запроса
@router.message(Command("support"))
async def cmd_start(message: Message):
    await db_start()
    await message.answer(
        "Напишите /get_support и опишите проблему в этом же сообщении. "
        "После чего оно будет перенаправлено в поддержку")