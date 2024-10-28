import datetime
import locale
import os

# Определяем операционную систему
if os.name == "nt":  # Windows
    locale.setlocale(locale.LC_TIME, "Russian_Russia.1251")
else:  # Linux или macOS
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# Получаем текущий день недели
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)

# Вывод текущего дня недели на русском
print(f"Сегодня: {today.strftime('%A')}")
print(f"Завтра: {tomorrow.strftime('%A')}")

# Получаем список дней до конца недели (включая сегодняшний)
days_left = (
    (today + datetime.timedelta(days=weekday_index)).strftime("%A")
    for weekday_index in range(7 - today.weekday())
)

print("\nДни до конца недели:")
for weekday_name in days_left:
    print(weekday_name.capitalize())

LOCALE_DAYNAMES = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}
print(datetime.datetime.now().strftime("%A"))
