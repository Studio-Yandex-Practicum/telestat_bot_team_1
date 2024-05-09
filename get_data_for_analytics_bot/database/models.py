from sqlalchemy import DateTime, String, func, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class UserTG(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    # user_id_tg: Mapped[str] = mapped_column(String(20), nullable=False)
    is_superuser: Mapped[str] = mapped_column(Boolean, default=False)
    is_admin: Mapped[str] = mapped_column(Boolean, default=False)


class ChannelTG(Base):
    __tablename__ = 'channel'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_channel_name: Mapped[str] = mapped_column(String(64), nullable=False)
