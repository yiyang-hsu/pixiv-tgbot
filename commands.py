from telegram import Bot, Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from creadcials import *
from utils import build_menu, like_buttons
from cloud import get_users

def start(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=chat_id, text="本子社的机器人~")
    bot.send_message(chat_id=chat_id, text="向我发送一张图片，我会附上两个反馈按钮发送到附带的 Channel，并且不会显示是谁发的。不过如果有谁做坏事，我就把他拉黑！")
    bot.send_message(chat_id=chat_id, text="现在支持直接分享给我来自 Pixiv 的链接来发送多张图片，但是暂不支持动图。")

def contributors(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    if (chat_id != GROUP):
        bot.send_message(chat_id=chat_id, text="该命令只能在本子社的 TG 群内部使用。")
    else:
        text = '*贡献榜 Top 10* \n'
        i = 0
        for user in get_users():
            i += 1
            text += "{} - {} - Points: {}\n".format(i, user.get('user_nick'), user.get('user_contrib'))
        text += '----------\n _Tips: 发布图片，或者对图片进行反馈都可以增加点数！_'
        bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)