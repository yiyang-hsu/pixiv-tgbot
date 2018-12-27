from telegram import Bot, Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from creadcials import *
from utils import build_menu, like_buttons

def start(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    message_id = bot.send_message(chat_id=chat_id, text="本子社的机器人~")