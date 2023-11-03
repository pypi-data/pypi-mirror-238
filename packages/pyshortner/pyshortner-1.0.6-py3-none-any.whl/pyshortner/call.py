from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
import requests
from config import *



shortner_link = WebAppInfo(url=f"https://{SHORTNER_LINK}/member/tools/api?bot=true")



START_MESSAGE_REPLY_MARKUP  = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📢 Channel', url=f'{CHANNEL_LINK}'),
        InlineKeyboardButton('📕 About', callback_data='about_dkbotz')
    ],
    [
        InlineKeyboardButton('💵 Balance', callback_data='dkbotz_balance')
    ],
    [
        InlineKeyboardButton('📙 Help', callback_data='help_dkbotz'),
        InlineKeyboardButton('⚙️ Settings', callback_data='dkbotz_settings')
    ],
    [
        InlineKeyboardButton('📡 Connect To Bot', web_app=shortner_link)
    ],
    [
        InlineKeyboardButton('🏞️ Switch To Old Panel 🏞️', callback_data='old_btn_dkbotz')
    ]
])

OLD_START_MESSAGE_REPLY_MARKUP  = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📢 Channel', url=f'{CHANNEL_LINK}'),
        InlineKeyboardButton('📕 About', callback_data='about_dkbotz')
    ],
    [
        InlineKeyboardButton('💵 Balance', callback_data='dkbotz_balance')
    ],
    [
        InlineKeyboardButton('📙 Help', callback_data='help_dkbotz'),
        InlineKeyboardButton('⚙️ Settings', callback_data='dkbotz_settings')
    ],
    [
        InlineKeyboardButton('📡 Connect To Bot', url=f"https://{SHORTNER_LINK}/member/tools/api?bot=true")
    ],
    [
        InlineKeyboardButton('🏞️ Switch To New Panel 🏞️', callback_data='new_btn_dkbotz')
    ]
])




