import telegram, requests, json, utils
import random
from creadcials import *

def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text("Hi! 这是本子社的 Bot !")
    update.message.reply_text("试试 /help ~")

def shota(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    image_info = utils.get_image_info();
    if (image_info):
        text = utils.format_shota_reply(image_info)
    else:
        text = '社长的网站还没好喔~'
    bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot, update):
    chat_id = update.message.chat_id
    help_text = '/help ----- 查看帮助\n/shota ----- 从图床获取一张图片\n/hughug ----- 抱抱~\n/getin ----- 进入本子社\n/view ----- 查看本 Bot 缓存的图片\n------------\nBug 请戳 @TyteKa'
    update.message.reply_text(help_text)
    bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def hughug(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    user_list = utils.get_user_list('list');
    button_list = []
    for item in user_list:
        button_list.append(telegram.InlineKeyboardButton(item['alias'] if item['alias'] else item['first_name'] , callback_data='hug/' + item['userid']))
    reply_markup = telegram.InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=3))
    bot.send_message(chat_id=chat_id, text="抱抱谁呢？", reply_markup=reply_markup, reply_to_message_id=update.message.message_id)

def getid(bot, update):
    chat_id = update.message.chat_id
    print(update)
    update.message.reply_text(chat_id)

def bebug(bot, update):
    chat_id = bzsgroup
    text = '开发中，可能会出现问题~\n*请暂停尝试吧！*'
    bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def debug(bot, update):
    chat_id = bzsgroup
    text = '结束 debug~'
    bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def getin(bot, update):
    chat_id = update.message.chat_id
    button_list = [telegram.InlineKeyboardButton('主站', url='https://www.benzishe.net/'),telegram.InlineKeyboardButton('图床', url='https://image.benzishe.net/')]
    reply_markup = telegram.InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=chat_id, text="从这里进入啦~", reply_markup=reply_markup, reply_to_message_id=update.message.message_id)

def nick(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    nick_name = ' '.join(update.message.text.split(' ')[1:])
    utils.update_nick(from_user, nick_name)
    text = '现在 [{firstname}](tg://user?id={userid}) 的昵称已经更新成了{nick}。'.format(firstname=from_user.first_name, nick=nick_name, userid = from_user.id)
    bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=update.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def members(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    user_list = utils.get_user_list('list')
    text = ''
    for item in user_list:
        text += str(item)
        text += '\n'
    update.message.reply_text(text)

def cached_image(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    if ( not ' ' in update.message.text):
        rowid = random.randint(1, 189)
    else:
        rowid = int(update.message.text.split(' ')[1])
    values = utils.format_view_reply(rowid)
    if values[0]:
        bot.send_message(chat_id=chat_id, text=values[0], reply_to_message_id=update.message.message_id, reply_markup=values[1],parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text("没有这张照片喔~")
