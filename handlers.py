from utils import confirm_buttons, get_image_info
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

    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    tags = []
    url = file = ''
    for entity in entities:
        entity_text = text[entity['offset']:entity['offset']+entity['length']]
        if entity['type'] == 'url':
            url = entity_text
            file, title, tags, artist = get_image_info(entity_text)

    if file == -1:
        return

    caption = '*{}* \nby {}\n'.format(title, artist)
    for tag in tags:
        caption += '#{} '.format(tag)
    caption += "[Link]({})".format(url)
    sent_message = bot.send_photo(
       chat_id=chat_id, photo=open(file, 'rb'), caption=caption, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=message_id)
    # sent_message = bot.send_message(
    #    chat_id=chat_id, text=caption, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=message_id)

    bot.send_message(chat_id=chat_id, text="您想要发送这张图片吗？", reply_to_message_id=sent_message['message_id'],
                     reply_markup=InlineKeyboardMarkup(buttons))
