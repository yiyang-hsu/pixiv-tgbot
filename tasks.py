from creadcials import *
import telegram, requests, json, utils
from random import randint

# Runs 8:00 every day
def shota_sch(bot, job):
    chat_id = bzsgroup
    image_info = utils.get_image_info()
    user_list = utils.get_user_list('list')
    index = randint(0, len(user_list))
    alias = user_list[index]['alias'] if user_list[index]['alias'] else user_list[index]['first_name']
    text = '早上好！今天 *{alias}* 抱走了下面这个正太~'.format(alias=alias)
    bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)
    rowid = randint(1, 189)
    values = utils.format_view_reply(rowid)
    bot.send_message(chat_id=chat_id, text=values[0], parse_mode=telegram.ParseMode.MARKDOWN)

def daily_sch(bot, job):
    shota_sch(bot, job)
