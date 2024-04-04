from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command('app'))
async def open_app(message: types.Message) -> None:
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='open app',
                                  web_app=WebAppInfo(
                                      url='https://alinlpkv.github.io/page/page.html'
                                  )
                                  )],
        ],
        resize_keyboard=True,
    )
    await message.answer('For create meeting', reply_markup=markup)


