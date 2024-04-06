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

    user_id = Column(ForeignKey('whitelist.user_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    meeting_id = Column(Integer, primary_key=True)
    meeting_theme = Column(Text, nullable=False, default='Напоминание')
    meeting_date_start = Column(DateTime, nullable=False)
    meeting_date_end = Column(DateTime, nullable=False)
    meeting_description = Column(Text)
    # user_email = Column(ForeignKey('whitelist.user_email', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user_email = Column(String(100), nullable=False)
