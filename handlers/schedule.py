from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import get_student_data
from utils import parse_all_schedules, translate_weekday

router = Router()


@router.message(F.text == "Расписание на сегодня 📚")
async def get_today_schedule(message: Message, session: AsyncSession) -> None:
    today = translate_weekday(datetime.now().strftime("%A"))
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = (await parse_all_schedules()).get(class_name)
    schedule_text = today + ":\n" + schedule.get(today, "Нет занятий   🥳")
    await message.answer(text=schedule_text)


@router.message(F.text == "Расписание на завтра 📚")
async def get_tomorrow_schedule(message: Message, session: AsyncSession) -> None:
    tomorrow = translate_weekday((datetime.now() + timedelta(days=1)).strftime("%A"))
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = (await parse_all_schedules()).get(class_name)
    schedule_text = tomorrow + ":\n" + schedule.get(tomorrow, "Нет занятий   🥳")
    await message.answer(schedule_text)


@router.message(F.text == "Расписание до конца недели 📚")
async def get_remaining_week_schedule(message: Message, session: AsyncSession) -> None:
    today = datetime.now()
    days_left = tuple(
        translate_weekday((today + timedelta(days=weekday_index)).strftime("%A"))
        for weekday_index in range(7 - today.weekday())
    )
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = (await parse_all_schedules()).get(class_name)
    schedule_text = ""
    for day in schedule:
        if day in days_left:
            schedule_text += "\n" + day + ":"
            schedule_text += "\n" + schedule[day] + "\n"
    await message.answer(schedule_text if schedule_text else "Занятий нет   🥳")


@router.message(F.text == "Расписание на всю неделю 📚")
async def get_full_week_schedule(message: Message, session: AsyncSession) -> None:
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    schedule = (await parse_all_schedules()).get(class_name)
    schedule_text = ""
    for day in schedule:
        schedule_text += "\n" + day + ":"
        schedule_text += "\n" + schedule[day] + "\n"
    await message.answer(schedule_text)
