from telegram import Bot, Update, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from creadcials import *
from utils import build_menu, like_buttons
from cloud import get_users

def start(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=chat_id, text="""1. 向我发送一张图片，我会附上两个反馈按钮发送到 Channel 。
2. 向我发送一个来自 Pixiv 链接，我会提取标签和链接发送到 Channel 。
3. 放心，发送之前都会要求你确认。
4. 实现了黑名单。
5. Bot 运行在 Heroku 的免费计划中，因此可能有点慢。请耐心。
---
1. Send the bot a picture and he will forward it to the Channel with two feedback buttons.
2. Send the bot a link from Pixiv and he will extract the image, tags and link, then forward them to the Channel.
3. Anyone will be asked to confirm before sending anything.
4. A blacklist has been implemented so don't be evil.
5. This bot is running in a free plan on Heroku, so it could be very slow. Please be patient.""", parse_mode=ParseMode.MARKDOWN)

def contributors(bot: Bot, update: Update):
    chat_id = update['message']['chat_id']
    if (chat_id != GROUP and chat_id != OWNER):
        bot.send_message(chat_id=chat_id, text="该命令只能在本子社的 TG 群内部使用。 Sorry, this command can be only used in a private group.")
    else:
        text = '*贡献榜 Top 10* \n'
        i = 0
        for user in get_users():
            i += 1
            text += "{} - {} - Points: {}\n".format(i, user.get('user_nick'), user.get('user_contrib'))
        text += '----------\n _Tips: 发布图片，或者对图片进行反馈都可以增加点数！_'
        bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)