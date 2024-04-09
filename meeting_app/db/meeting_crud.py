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
        user_id = int(data.get('user_id'))
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

        query = (select(UserMeeting.meeting_theme, UserMeeting.meeting_date_start).
                 where(UserMeeting.user_id==user_id).
                 where(UserMeeting.meeting_date_end > dt.datetime.now()))
        with self.engine.connect() as conn:
            meetings = conn.execute(query)

        return MeetingCRUD.data_as_dict(meetings)

    @staticmethod
    def data_as_dict(data: CursorResult) -> list[dict[str, Any]]:
        """Преобразование результата запроса в список из словарей, где ключи - имена полей"""
        return [data_part._asdict() for data_part in data]