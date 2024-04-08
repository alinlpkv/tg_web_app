import datetime as dt
from typing import Any

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Request,
)

from database import MeetingCRUD
from send_meeting import SmtpSend
from constans import DEFAULT_THEME

app = Flask(__name__)


def format_date(data):
    for i, row in enumerate(data):
        data[i]['meeting_date_start'] = row['meeting_date_start'].strftime('%d.%m.%y %H:%M')
    return data


@app.route('/<user_id>', methods=['GET'])
async def show_meetings(user_id):
    if user_id is not None:
        meeting_crud = MeetingCRUD()
        meetings = await meeting_crud.get_user_meetings(int(user_id))
        meetings = format_date(meetings)
        return render_template('meeting.html', meetings=meetings, user_id=user_id)
    else:
        return 'Отсутствует User ID.'


@app.route('/<user_id>/create', methods=['GET', 'POST'])
async def create_meeting(user_id):
    if request.method == 'POST':
        data = reformat_data(request)
        meeting_crud = MeetingCRUD()
        user_email = await meeting_crud.get_user_email(user_id=int(user_id))
        data['user_id'] = int(user_id)
        data['user_email'] = user_email
        await meeting_crud.add_meeting(data)
        SmtpSend().send_meeting(data)
        return redirect(url_for('show_meetings', user_id=user_id))
    return render_template('create.html', user_id=user_id)


def reformat_data(request_: Request) -> dict[str: Any]:
    """
    Получение и преобразование данных из формы

    :param request_: Request с данными из формы
    :return: отформатированные данные
    """
    date_picker_frmt = '%d.%m.%Y %H:%M'
    data = dict()

    data['meeting_theme'] = request_.form['meeting_theme'] if request_.form['meeting_theme'] else DEFAULT_THEME
    data['meeting_description'] = request_.form['meeting_description']
    data['meeting_date_start'] = dt.datetime.strptime(request_.form['meeting_date_start'], date_picker_frmt)
    data['meeting_date_end'] = dt.datetime.strptime(request_.form['meeting_date_end'], date_picker_frmt) \
        if request_.form['meeting_date_end'] \
        else data['meeting_date_start'] + dt.timedelta(minutes=1)
    data['timezone'] = int(request.form['timezoneOffset']) / 60
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)


# 342297636