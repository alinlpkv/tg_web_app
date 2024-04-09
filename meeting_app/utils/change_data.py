import datetime as dt
from typing import Any

from flask import Request

from constans import DEFAULT_THEME, DATE_PICKER_FORMAT


def format_date(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Преобразование времени начала встречи в определенный формат.

    :param data: данные о встречах пользователя
    return: данные о встречах пользователя с новым форматом времени начала
    """
    for i, row in enumerate(data):
        data[i]['meeting_date_start'] = row['meeting_date_start'].strftime(DATE_PICKER_FORMAT)
    return data


def reformat_data(request_: Request) -> dict[str: Any]:
    """
    Получение и преобразование данных из формы

    :param request_: Request с данными из формы
    :return: отформатированные данные
    """
    data = dict()

    data['meeting_theme'] = request_.form['meeting_theme'] if request_.form['meeting_theme'] else DEFAULT_THEME
    data['meeting_description'] = request_.form['meeting_description']
    data['meeting_date_start'] = dt.datetime.strptime(request_.form['meeting_date_start'], DATE_PICKER_FORMAT)
    data['meeting_date_end'] = dt.datetime.strptime(request_.form['meeting_date_end'], DATE_PICKER_FORMAT) \
        if request_.form['meeting_date_end'] \
        else data['meeting_date_start'] + dt.timedelta(minutes=1)
    data['timezone'] = int(request_.form['timezoneOffset']) / 60
    return data