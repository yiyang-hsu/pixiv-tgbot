from utils import confirm_buttons
from telegram import Bot, Update, ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton


def photo_handler(bot: Bot, update: Update):
    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']
    bot.send_message(chat_id=chat_id, text="您想要发送这张图片吗？", reply_to_message_id=message_id,
                     reply_markup=InlineKeyboardMarkup(buttons))


def entity_handler(bot: Bot, update: Update):
    buttons = confirm_buttons()

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']

    text = update['message']['text']
    entities = update['message']['entities']

    tags = []
    url = image_url = ''
    for entity in entities:
        entity_text = text[entity['offset']:entity['offset']+entity['length']]
        if entity['type'] == 'url':
            url = entity_text
            image_url = entity_text
        elif entity['type'] == 'hashtag':
            tags.append(entity_text)

    if url == '' or image_url == '':
        return

    caption = '[Link]({})'.format(url)
    for tag in tags:
        caption += ' {}'.format(tag)

    sent_message = bot.send_message(
        chat_id=chat_id, text=caption, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=message_id)
    bot.send_message(chat_id=chat_id, text="您想要发送这个吗？", reply_to_message_id=sent_message['message_id'],
                     reply_markup=InlineKeyboardMarkup(buttons))