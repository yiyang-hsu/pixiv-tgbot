from utils import confirm_buttons, get_image_info, build_menu
from telegram import Bot, Update, ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from os import remove
from creadcials import OWNER


def monitor(bot, chat_id, message_id):
    bot.forward_message(chat_id=OWNER, from_chat_id=chat_id,
                        message_id=message_id, disable_notification=True)


def photo_handler(bot: Bot, update: Update):
    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']

    monitor(bot, chat_id, message_id)
    bot.send_message(chat_id=chat_id, text="您想要发送这个吗？", reply_to_message_id=message_id,
                     reply_markup=InlineKeyboardMarkup(buttons))


def entity_handler(bot: Bot, update: Update):
    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']

    monitor(bot, chat_id, message_id)

    text = update['message']['text']
    entities = update['message']['entities']

    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    tags = []
    url = file = ''
    for entity in entities:
        entity_text = text[entity['offset']:entity['offset']+entity['length']]
        if entity['type'] == 'url':
            url = entity_text
            images = get_image_info(entity_text)

    if images == {}:
        return

    caption = '*{}* \n作者: {}\n'.format(images['title'], images['artist'])
    for tag in images['tags']:
        caption += '#{} '.format(tag)
    caption += "[链接]({})".format(images['url'])
    count = len(images['files'])
    if count == 1:
        sent_message = bot.send_photo(
            chat_id=chat_id, photo=open(images['files'][0], 'rb'), caption=caption, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=message_id, timeout=40)

        bot.send_message(chat_id=chat_id, text="您想要发送这个吗？", reply_to_message_id=sent_message['message_id'],
                         reply_markup=InlineKeyboardMarkup(buttons))
    else:
        current = 0
        groups = build_menu(images['files'], n_cols=10)
        sent_messages = []
        for group in groups:
            sent_messages += bot.send_media_group(
                chat_id=chat_id, media=[InputMediaPhoto(open(file, 'rb'), caption='({}/{}) '.format(images['files'].index(file) + 1, count) + caption, parse_mode=ParseMode.MARKDOWN) for file in group], reply_to_message_id=message_id, timeout=600)

        for sent_message in sent_messages:
            bot.send_message(chat_id=chat_id, text="您想要发送这个吗？", reply_to_message_id=sent_message['message_id'],
                             reply_markup=InlineKeyboardMarkup(buttons), timeout=600)
        for file in images['files']:
            remove(file)
