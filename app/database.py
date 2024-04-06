import asyncio
import os
import datetime as dt
from typing import Any

import pytz
from sqlalchemy import text, select, insert
from sqlalchemy.ext.asyncio import create_async_engine

from app.models import UserMeeting, Whitelist


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
        # query = text('insert into meeting (user_id, name, description, date, user_email) '
        #              'values (:user_id, :name, :description, :date, :user_email)')
        async with self.engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()

# async def s():
#     import os
#     from dotenv import load_dotenv
#     from sqlalchemy.ext.asyncio import create_async_engine
#     load_dotenv()
#     engine = create_async_engine(os.getenv('DATA_BASE_URL'))
#     m = MeetingCRUD(engine)
#     await m.get_user_email(342297636)
#     await
#
#
# if __name__ == '__main__':
#     asyncio.run(s())
