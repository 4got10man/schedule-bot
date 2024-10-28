from sqlalchemy import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    class_name: Mapped[str] = mapped_column(VARCHAR(4), nullable=False)
    notification_time: Mapped[str] = mapped_column(VARCHAR(5), nullable=True)
