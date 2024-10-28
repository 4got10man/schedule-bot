from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import get_all_students_data, get_student_data
from utils import parse_schedule, translate_weekday

router = Router()


@router.message(F.text == "Расписание на сегодня 📚")
async def get_today_schedule(message: Message, session: AsyncSession) -> None:
    today = translate_weekday(datetime.now().strftime("%A"))
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = parse_schedule(class_name.split("_")[0])
    schedule_text = today + ":\n" + schedule[class_name].get(today, "Нет занятий   🥳")
    await message.answer(text=schedule_text)


@router.message(F.text == "Расписание на завтра 📚")
async def get_tomorrow_schedule(message: Message, session: AsyncSession) -> None:
    tomorrow = translate_weekday((datetime.now() + timedelta(days=1)).strftime("%A"))
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = parse_schedule(class_name.split("_")[0])
    schedule_text = (
        tomorrow + ":\n" + schedule[class_name].get(tomorrow, "Нет занятий   🥳")
    )
    await message.answer(schedule_text)


@router.message(F.text == "Расписание до конца недели 📚")
async def get_remaining_week_schedule(message: Message, session: AsyncSession) -> None:
    today = datetime.now()
    days_left = tuple(
        translate_weekday((today + timedelta(days=weekday_index)).strftime("%A"))
        for weekday_index in range(7 - today.weekday())
    )
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = parse_schedule(class_name.split("_")[0])
    schedule_text = ""
    for day in schedule[class_name]:
        if day in days_left:
            schedule_text += "\n" + day + ":"
            schedule_text += "\n" + schedule[class_name][day] + "\n"
    await message.answer(schedule_text if schedule_text else "Занятий нет   🥳")


@router.message(F.text == "Расписание на всю неделю 📚")
async def get_full_week_schedule(message: Message, session: AsyncSession) -> None:
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = parse_schedule(class_name.split("_")[0])
    schedule_text = ""
    for day in schedule[class_name]:
        schedule_text += "\n" + day + ":"
        schedule_text += "\n" + schedule[class_name][day] + "\n"
    await message.answer(schedule_text)
