import datetime as dt
from typing import Any

from sqlalchemy import select, insert, CursorResult

from db.models import UserMeeting, Whitelist
from db.engine import engine


class MeetingCRUD:

    def __init__(self):
        self.engine = engine

    def get_user_email(self, user_id: int | str) -> str:
        """
        Получение почты пользователя по его id.

        :param user_id: id пользователя
        :return: почта пользователя
        """
        if isinstance(user_id, str):
            user_id = int(user_id)

        with self.engine.connect() as conn:
            query = select(Whitelist.user_email).where(Whitelist.user_id==user_id)
            email = conn.execute(query)
        return email.scalar()

    def add_meeting(self, data: dict[str, Any]) -> None:
        """
        Добавление новой встречи пользователя в бд.

        :param data: данные о встрече
        """

        query = insert(UserMeeting).values(
            user_id=int(data.get('user_id')),
            theme=data.get('theme'),
            description=data.get('description'),
            date_start=data.get('date_start'),
            date_end=data.get('date_end')
        )
        with self.engine.connect() as conn:
            conn.execute(query)
            conn.commit()

    def get_user_meetings(self, user_id: int | str) -> list[dict[str, Any]]:
        """
        Получение всех предстоящих и идущих встреч пользователя.

        :param user_id: id пользователя
        :return: Список из словарей с информацией о встречах
        """
        if isinstance(user_id, str):
            user_id = int(user_id)

        query = (select(UserMeeting.theme, UserMeeting.date_start).
                 where(UserMeeting.user_id==user_id).
                 where(UserMeeting.date_end > dt.datetime.now()))
        with self.engine.connect() as conn:
            meetings = conn.execute(query)

            return MeetingCRUD.data_as_dict(meetings)

    @staticmethod
    def data_as_dict(data: CursorResult) -> list[dict[str, Any]]:
        """Преобразование результата запроса в список из словарей, где ключи - имена полей"""
        return [data_part._asdict() for data_part in data]