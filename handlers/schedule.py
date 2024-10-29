from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from utils import (
    get_days_until_end_of_week,
    get_schedule_for_day,
    get_schedule_for_days,
)

router = Router()


@router.message(F.text == "Расписание на сегодня 📚")
async def get_today_schedule(message: Message, session: AsyncSession) -> None:
    await get_schedule_for_day(message, session)


@router.message(F.text == "Расписание на завтра 📚")
async def get_tomorrow_schedule(message: Message, session: AsyncSession) -> None:
    await get_schedule_for_day(message, session, day="tomorrow")


@router.message(F.text == "Расписание до конца недели 📚")
async def get_remaining_week_schedule(message: Message, session: AsyncSession) -> None:
    remaining_days = await get_days_until_end_of_week()
    await get_schedule_for_days(message, session, remaining_days=remaining_days)


@router.message(F.text == "Расписание на всю неделю 📚")
async def get_full_week_schedule(message: Message, session: AsyncSession) -> None:
    await get_schedule_for_days(message, session)
