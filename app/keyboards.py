from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Reply клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получить геолокацию"),
     KeyboardButton(text="Посмотреть карту")]
])