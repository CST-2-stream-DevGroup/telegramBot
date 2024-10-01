from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#Reply клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получить геолокацию")],
    [KeyboardButton(text="Посмотреть карту")],
],resize_keyboard = True)