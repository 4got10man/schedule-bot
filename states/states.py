from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    telegram_id = State()
    class_name = State()
    notification_time = State()


class UserUpdates(StatesGroup):
    change_notification_time = State()
    change_class_name = State()
