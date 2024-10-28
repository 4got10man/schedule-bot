from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import get_all_students_data
from utils import parse_schedule, translate_weekday

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def send_daily_notifications(class_name: str, bot: Bot, telegram_id: int) -> None:
    tomorrow = translate_weekday((datetime.now() + timedelta(days=1)).strftime("%A"))
    schedule = parse_schedule(class_name.split("_")[0])
    schedule_text = (
        tomorrow + ":\n" + schedule[class_name].get(tomorrow, "Нет занятий   🥳")
    )
    await bot.send_message(telegram_id, schedule_text)


async def schedule_daily_notifications(session: AsyncSession, bot: Bot) -> None:
    students = await get_all_students_data(session)
    for student in students:
        await add_notification(
            student.telegram_id,
            student.class_name,
            student.notification_time,
            bot,
        )


async def add_notification(
    telegram_id: int, class_name: str, notification_time: str, bot: Bot
) -> None:
    job_id = f"{telegram_id}_notification"
    job = scheduler.get_job(job_id)
    if job:
        scheduler.remove_job(job_id)
    print(f"{notification_time = }")
    if notification_time is None:
        return
    hour, minute = notification_time.split(":")
    scheduler.add_job(
        send_daily_notifications,
        "cron",
        hour=hour,
        minute=minute,
        id=job_id,
        kwargs={"class_name": class_name, "bot": bot, "telegram_id": telegram_id},
    )
