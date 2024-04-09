
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

from db.meeting_crud import MeetingCRUD
from utils.send_meeting import SmtpSend
from utils.change_data import format_date, reformat_data

app = Flask(__name__)


@app.route('/')
async def hello():
    return 'Empty page.'


@app.route('/meeting')
async def meeting():
    return "It's web meeting app."


@app.route('/meeting/<user_id>', methods=['GET'])
async def show_meetings(user_id: str):
    if user_id is not None:
        meetings = await meeting_crud.get_user_meetings(user_id)
        meetings = format_date(meetings)
        return render_template('meeting.html', meetings=meetings, user_id=user_id)
    else:
        return 'Отсутствует User ID.'


@app.route('/meeting/<user_id>/create', methods=['GET', 'POST'])
async def create_meeting(user_id: str):
    if request.method == 'POST':
        data = reformat_data(request)
        user_email = await meeting_crud.get_user_email(user_id=user_id)
        print(user_email)
        data['user_id'] = user_id
        data['user_email'] = user_email
        await meeting_crud.add_meeting(data)
        SmtpSend().send_meeting(data)
        return redirect(url_for('show_meetings', user_id=user_id))
    return render_template('create.html', user_id=user_id)


if __name__ == '__main__':
    meeting_crud = MeetingCRUD()
    app.run(host='0.0.0.0', port=9000)


# 342297636