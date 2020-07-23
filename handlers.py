from utils import confirm_buttons, get_image_info, build_menu
from telegram import Bot, Update, ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from os import remove
from credentials import OWNER, WHITELIST
from googletrans import Translator
from cloud import if_blocked


def monitor(bot, chat_id, message_id):
    bot.forward_message(chat_id=OWNER, from_chat_id=chat_id,
                        message_id=message_id, disable_notification=True)


def filter(bot, chat_id):
    if (chat_id in WHITELIST):
        return True
    elif (if_blocked(chat_id)):
        bot.send_message(
            chat_id=chat_id, text="_Sorry but you have been banned._", parse_mode=ParseMode.MARKDOWN)
        return False


def photo_handler(bot: Bot, update: Update):

    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']

    if filter(bot, chat_id):
        pass
    else:
        return

    # monitor(bot, chat_id, message_id)
    bot.send_message(chat_id=chat_id, text="您想要发送这个吗？/ Would you like to send this?", reply_to_message_id=message_id,
                     reply_markup=InlineKeyboardMarkup(buttons))


def tags_handler(tags):
    tags_text = ''
    for tag in tags:
        tag = tag.replace('-', '')
        tags_text += '#{} '.format(tag)
    return tags_text


def entity_handler(bot: Bot, update: Update):
    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']

    if filter(bot, chat_id):
        pass
    else:
        return

    # monitor(bot, chat_id, message_id)

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
    print(images['tags'])
    caption += tags_handler(images['tags'])
    print(caption)
    caption += "\n{}".format(images['url'][8::])
    count = len(images['files'])
    if count == 1:
        sent_message = bot.send_photo(
            chat_id=chat_id, photo=open(images['files'][0], 'rb'), caption=caption, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=message_id, timeout=40)

        bot.send_message(chat_id=chat_id, text="您想要发送这个吗？/ Would you like to send this?", reply_to_message_id=sent_message['message_id'],
                         reply_markup=InlineKeyboardMarkup(buttons))
    else:
        current = 0
        groups = build_menu(images['files'], n_cols=10)
        sent_messages = []
        for group in groups:
            sent_messages += bot.send_media_group(
                chat_id=chat_id, media=[InputMediaPhoto(open(file, 'rb'), caption='({}/{}) '.format(images['files'].index(file) + 1, count) + caption, parse_mode=ParseMode.MARKDOWN) for file in group], reply_to_message_id=message_id, timeout=600)

        for sent_message in sent_messages:
            bot.send_message(chat_id=chat_id, text="您想要发送这个吗？/ Would you like to send this? ", reply_to_message_id=sent_message['message_id'],
                             reply_markup=InlineKeyboardMarkup(buttons), timeout=600)
        for file in images['files']:
            remove(file)
