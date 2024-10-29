from datetime import datetime, timedelta

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import get_student_data
from utils import get_cached_schedule, translate_weekday


async def get_student_schedule(message: Message, session: AsyncSession) -> dict:
    class_name = await get_student_data(session, message.from_user.id, "class_name")
    return (await get_cached_schedule()).get(class_name)


async def get_schedule_for_day(
    message: Message, session: AsyncSession, day: str = "today"
) -> None:
    target_date = datetime.now()
    if day == "tomorrow":
        target_date = target_date + timedelta(days=1)
    day_name = translate_weekday(target_date.strftime("%A"))
    schedule = await get_student_schedule(message, session)
    schedule_text = day_name + ":\n" + schedule.get(day_name, "Нет занятий   🥳")
    await message.answer(schedule_text)


async def get_days_until_end_of_week():
    today = datetime.now()
    remaining_days = tuple(
        translate_weekday((today + timedelta(days=weekday_index)).strftime("%A"))
        for weekday_index in range(7 - today.weekday())
    )
    return remaining_days


async def get_schedule_for_days(
    message: Message, session: AsyncSession, remaining_days: tuple | None = None
) -> None:
    schedule = await get_student_schedule(message, session)
    schedule_lines = []
    for day in schedule:
        if remaining_days is None or day in remaining_days:
            schedule_lines.append("\n" + day + ":")
            schedule_lines.append(schedule[day])
    schedule_text = "\n".join(schedule_lines)
    await message.answer(schedule_text if schedule_text else "Занятий нет   🥳")
