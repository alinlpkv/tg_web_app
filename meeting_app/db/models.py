from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    String,
    BigInteger
)

Base = declarative_base()


class Whitelist(Base):
    __tablename__ = 'whitelist'

    user_id = Column(BigInteger, primary_key=True)
    user_email = Column(String(100), nullable=False, unique=True)


class UserMeeting(Base):
    __tablename__ = 'user_meeting'
    __table_args__ = {'comment': 'Перечень встреч пользователей'}

    # TODO: работа с таймзоной по отправке уведомлений
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('whitelist.user_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    theme = Column(Text, nullable=False, default='Напоминание', comment='Тема встречи')
    date_start = Column(DateTime, nullable=False, comment='Время начала встречи')
    date_end = Column(DateTime, nullable=False, comment='Время окончания встречи')
    description = Column(Text, comment='Описание встречи')
