from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#Reply клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Добавить метку")],
    [KeyboardButton(text="Посмотреть карту")],
],resize_keyboard = True)

my_loc = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить локацию", request_location = True)],
],resize_keyboard = True, one_time_keyboard=True)

