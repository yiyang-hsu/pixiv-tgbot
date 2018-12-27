from telegram import Bot, Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from creadcials import *
from utils import build_menu, like_buttons

def start(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=chat_id, text="本子社的机器人~")
    bot.send_message(chat_id=chat_id, text="向我发送一张图片，我会附上两个反馈按钮发送到附带的 Channel，并且不会显示是谁发的。不过如果有谁做坏事，我就把他拉黑！")