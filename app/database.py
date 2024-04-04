import asyncio
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


class MeetingCRUD:

    def __init__(self):
        self.engine = create_async_engine(os.getenv('DATA_BASE_URL'))

    async def get_user_email(self, user_id):
        async with self.engine.connect() as conn:
            email = await conn.execute(text(f'select user_email from whitelist where user_id={user_id}'))
        return email.scalar()

    async def add_meeting(self, data: dict):
        user_id = data.get('user_id')
        name = data.get('name')
        description = data.get('description')
        date = data.get('date')
        user_email = data.get('user_email')
        query = text('insert into meeting (user_id, name, description, date, user_email) '
                     'values (:user_id, :name, :description, :date, :user_email)')
        async with self.engine.connect() as conn:
            await conn.execute(query.bindparams(
                user_id=user_id, name=name, description=description, date=date, user_email=user_email))
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
