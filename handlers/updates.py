from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import update_student_data
from keyboards import keyboard as kb
from notifications import add_notification
from states import UserUpdates
from utils import validate_class_name, validate_time

router = Router()


@router.message(F.text == "Изменить время уведомлений ⚙️")
async def change_notification_time(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите время уведомлений в формате HH:MM, например 19:00. "
        "Если же регулярные уведомления не нужны, введите слово 'нет'."
    )
    await state.set_state(UserUpdates.change_notification_time)


@router.message(UserUpdates.change_notification_time)
async def set_notification_time(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
) -> None:
    await validate_time(message, state)
    data = await state.get_data()
    notification_time = data["notification_time"]
    student = await update_student_data(
        session, message.from_user.id, "notification_time", notification_time
    )
    await message.answer(
        "Спасибо, данные обновлены.\n"
        f"Время уведомлений: {student.notification_time or 'уведомления отключены'}",
        reply_markup=kb.as_markup(resize_keyboard=True),
    )
    await add_notification(
        student.telegram_id,
        student.class_name,
        student.notification_time,
        bot,
    )
    await state.clear()


@router.message(F.text == "Изменить номер класса ⚙️")
async def weekly_schedule_message(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Ведите название вашего класса, в соответствии с тем, как оно указано "
        "на https://www.lit.msu.ru/study/timetable/, например 5_1, 6_2, 7_3 и т.п."
    )
    await state.set_state(UserUpdates.change_class_name)


@router.message(UserUpdates.change_class_name)
async def set_class_name(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
) -> None:
    telegram_id = message.from_user.id
    await validate_class_name(message, state)
    data = await state.get_data()
    class_name = data["class_name"]
    student = await update_student_data(session, telegram_id, "class_name", class_name)
    await message.answer(
        "Спасибо, данные обновлены.\n" f"Номер вашего класса: {student.class_name}",
        reply_markup=kb.as_markup(resize_keyboard=True),
    )
    await add_notification(
        student.telegram_id,
        student.class_name,
        student.notification_time,
        bot,
    )
    await state.clear()
