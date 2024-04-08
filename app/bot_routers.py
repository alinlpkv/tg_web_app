from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json
from typing import Union, Dict, Any
from aiogram.filters import Filter
from aiogram.types import Message
from app.database import MeetingCRUD
from app.constans import DEFAULT_THEME
from app.send_meeting import SmtpSend

router = Router()


@router.message(Command('app'))
async def open_app(message: types.Message) -> None:
    app_url = 'https://alinlpkv.github.io/tg_web_app/app/static/page.html'
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [types.KeyboardButton(text='Мои встречи', web_app=WebAppInfo(url=app_url))],
        ]
    )
    await message.answer('Для работы со встречами нажмите', reply_markup=markup)


@router.message(F.web_app_data)
async def web_app(message: types.Message):
    user_id = message.from_user.id
    data = json.loads(message.web_app_data.data)
    data = validate_data(data)

    await message.answer(f'Встреча создана!')

    meeting_crud = MeetingCRUD()
    user_email = await meeting_crud.get_user_email(user_id=user_id)

    data['user_id'] = user_id
    data['user_email'] = user_email
    send_meeting(data)
    # await meeting_crud.add_meeting(data)


def validate_data(data):
    import datetime as dt
    # import pytz
    meeting_theme = data.get('meeting_theme', DEFAULT_THEME)
    meeting_date_start = data.get('meeting_date_start')
    meeting_date_end = data.get('meeting_date_end')
    meeting_date_start = dt.datetime.strptime(meeting_date_start, '%d.%m.%Y %H:%M')
    meeting_date_end = dt.datetime.strptime(meeting_date_end, '%d.%m.%Y %H:%M')
    # meeting_date_start = meeting_date_start.replace(tzinfo=pytz.utc)
    # meeting_date_end = meeting_date_end.replace(tzinfo=pytz.utc)
    data['meeting_theme'] = meeting_theme
    data['meeting_date_start'] = meeting_date_start
    data['meeting_date_end'] = meeting_date_end
    return data


def send_meeting(data):
    SmtpSend().send_meeting(data)




# TODO: если второе поле даты пустое - заполнить на +1 минуту
# TODO: проверка на заполненность и соответствие форматов
# TODO: встреча прошла/не прошла флажок
# TODO: напоминалки
