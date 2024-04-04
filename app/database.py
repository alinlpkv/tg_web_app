from sqlalchemy import text

from main import engine





class MeetingCRUD:


    async def get_user_email(self, user_id):
        async with engine.connect() as conn:
            email = await conn.execute(text(f'select user_email from whitelist where user_id={user_id}'))
        return email

    async def add_meeting(self, data: dict):
        user_id = data.get('user_id')
        name = data.get('name')
        description = data.get('description')
        date = data.get('date')
        user_email = data.get('user_email')
        query = text('insert into meeting (user_id, name, description, date, user_email) '
                     'values (:user_id, :name, :description, :date, :user_email)')
        async with engine.connect() as conn:
            await conn.execute(query.bindparams(
                user_id=user_id, name=name, description=description, date=date, user_email=user_email))
            await conn.commit()
