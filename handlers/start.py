from aiogram import Bot, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import add_student, get_student_data
from keyboards import keyboard as kb
from states import UserRegistration
from utils import add_notification, validate_class_name, validate_time

router = Router()


@router.message(CommandStart())
async def command_start_handler(
    message: Message, session: AsyncSession, state: FSMContext
) -> None:
    data = await get_student_data(session, message.from_user.id)
    if data is not None:
        await message.answer(
            f"Вы уже зарегистрированы. Ваши данные:\n"
            f"Класс: {data.class_name}\n"
            f"Время уведомлений: {data.notification_time or 'уведомления отключены'}\n"
            "Для изменения данных воспользуйтесь экранной клавиатурой.",
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
        return
    await state.set_state(UserRegistration.telegram_id)
    await state.update_data(telegram_id=message.from_user.id)
    await state.set_state(UserRegistration.class_name)
    await message.answer(
        f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
        "Этот бот показывает расписание занятий Лицея информационных технологий "
        "(ЛИТ) 1533.\nРасписание взято с https://www.lit.msu.ru/study/timetable/."
        "\nДля получения расписания, ведите название вашего класса, в соответствии "
        "с тем, как оно указано на сайте, например 5_1, 6_2, 7_3 и т.п."
    )


@router.message(UserRegistration.class_name)
async def get_class_name(message: Message, state: FSMContext) -> None:
    await validate_class_name(message, state)
    data = await state.get_data()
    if not data.get("class_name"):
        return
    await state.set_state(UserRegistration.notification_time)
    await message.answer(
        "Если Вы хотите получать регулярные уведомления с расписанием уроков на "
        "следующий день, введите время уведомлений в формате HH:MM, например 19:00. "
        "Если регулярные уведомления не нужны, либо Вы хотите настроить их позднее, "
        "введите слово 'нет'."
    )


@router.message(UserRegistration.notification_time)
async def get_notification_time(
    message: Message, session: AsyncSession, state: FSMContext, bot: Bot
) -> None:
    await validate_time(message, state)
    data = await state.get_data()
    telegram_id = data["telegram_id"]
    class_name = data["class_name"]
    notification_time = data["notification_time"]

    await add_notification(telegram_id, class_name, notification_time, bot)

    await message.answer(
        "Спасибо, регистрация завершена. Ваши данные:\n"
        f"Класс: {class_name}\n"
        f"Время уведомлений: {notification_time or 'уведомления отключены'}",
        reply_markup=kb.as_markup(resize_keyboard=True),
    )
    await add_student(
        session,
        telegram_id=telegram_id,
        class_name=class_name,
        notification_time=notification_time,
    )
    await state.clear()
