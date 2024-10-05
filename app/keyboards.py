from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#Reply клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Добавить метку", request_location=True)],
    [KeyboardButton(text="Посмотреть карту")],
],resize_keyboard = True)