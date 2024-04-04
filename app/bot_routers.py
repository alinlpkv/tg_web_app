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

router = Router()


@router.message(Command('app'))
async def open_app(message: types.Message) -> None:
    app_url = 'https://alinlpkv.github.io/tg_web_app/app/static/page.html'
    markup = types.InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [types.InlineKeyboardButton(text='open app', web_app=WebAppInfo(url=app_url))],
        ]
    )
    await message.answer('For create meeting', reply_markup=markup)


@router.message(F.web_app_data)
async def web_app(message: types.Message):
    data = json.loads(message.web_app_data.data)
    print(data)
    meeting_name = data.get('meeting_name')
    await message.answer(f'Meeting "{meeting_name}" created!')

