from datetime import datetime
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .async_schedule_parser import parse_all_schedules


async def validate_time(message: Message, state: FSMContext) -> None:
    if message.text.strip().lower() == "нет":
        await state.update_data(notification_time=None)
    else:
        try:
            entered_time = datetime.strptime(message.text, "%H:%M").time()
        except ValueError:
            await message.answer(
                "Время введено некорректно. Введите время в формате HH:MM, либо "
                "слово 'нет', если сейчас уведомления не нужны."
            )
            return
        await state.update_data(notification_time=entered_time.strftime("%H:%M"))


async def validate_class_name(message: Message, state: FSMContext) -> None:
    valid_class_names = (await parse_all_schedules()).keys()
    if message.text.strip() not in valid_class_names:
        await message.answer(
            "Номер класса введен некорректно. Введите номер класса, для которого "
            "размещено расписание на https://www.lit.msu.ru/study/timetable/, в "
            "формате 5_1, 6_2, 7_3 и т.п."
        )
        return
    else:
        await state.update_data(class_name=message.text)
