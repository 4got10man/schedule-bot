from typing import Any

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Student


async def get_student_data(
    session: AsyncSession, telegram_id: int, field: str | None = None
) -> Any:
    data = await session.get(Student, telegram_id)
    return getattr(data, field) if field else data


async def add_student(
    session: AsyncSession,
    telegram_id: int,
    class_name: str,
    notification_time: str,
) -> None:
    new_student = Student(
        telegram_id=telegram_id,
        class_name=class_name,
        notification_time=notification_time,
    )
    session.add(new_student)
    await session.commit()


async def update_student_data(
    session: AsyncSession, telegram_id: int, field: str, value: str
) -> Student:
    student = await session.get(Student, telegram_id)
    setattr(student, field, value)
    await session.commit()
    return student


async def get_all_students_data(session: AsyncSession) -> ScalarResult[Student]:
    students = await session.scalars(select(Student))
    return students
