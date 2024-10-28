from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    KeyboardButton(text="Расписание на сегодня 📚"),
    KeyboardButton(text="Расписание на завтра 📚"),
    KeyboardButton(text="Расписание до конца недели 📚"),
    KeyboardButton(text="Расписание на всю неделю 📚"),
    KeyboardButton(text="Изменить время уведомлений ⚙️"),
    KeyboardButton(text="Изменить номер класса ⚙️"),
).adjust(2)
