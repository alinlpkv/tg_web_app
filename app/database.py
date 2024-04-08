import asyncio
import os
import datetime as dt
from typing import Any

import pytz
from sqlalchemy import text, select, insert
from sqlalchemy.ext.asyncio import create_async_engine

from models import UserMeeting, Whitelist


class MeetingCRUD:

    def __init__(self):
        self.engine = create_async_engine(os.getenv('DATA_BASE_URL'))

    async def get_user_email(self, user_id):
        async with self.engine.connect() as conn:
            query = select(Whitelist.user_email).where(Whitelist.user_id==user_id)
            email = await conn.execute(query)
        return email.scalar()

    async def add_meeting(self, data: dict[Any]):
        user_id = data.get('user_id')
        user_email = data.get('user_email')
        meeting_theme = data.get('meeting_theme')
        meeting_description = data.get('meeting_description')
        meeting_date_start = data.get('meeting_date_start')
        meeting_date_end = data.get('meeting_date_end')

        query = insert(UserMeeting).values(
            user_id=user_id,
            user_email=user_email,
            meeting_theme=meeting_theme,
            meeting_description=meeting_description,
            meeting_date_start=meeting_date_start,
            meeting_date_end=meeting_date_end
        )
        async with self.engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()

    async def get_user_meetings(self, user_id: int):
        query = (select(UserMeeting.meeting_theme, UserMeeting.meeting_date_start).
                 where(UserMeeting.user_id==user_id).
                 where(UserMeeting.meeting_date_end > dt.datetime.now())
                 )
        async with self.engine.connect() as conn:
            meetings = await conn.execute(query)

        return MeetingCRUD.data_as_dict(meetings)

    @staticmethod
    def data_as_dict(data) -> list[dict]:
        data_list = []
        for data_part in data:
            data_list.append(data_part._asdict())
        return data_list
