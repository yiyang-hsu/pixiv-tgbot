from cloud import add_user, check_feedback, get_feedback, init_message, add_picture
from utils import like_buttons, debug
from telegram import Bot, Update, ParseMode, Message, File
from credentials import CHANNEL, OWNER, CHANNEL_PUBLICNAME, UPLOAD_TOKEN, UPLOAD_URL
import requests


def callback_dispatcher(bot: Bot, update: Update):

    call_data = update.callback_query['data'].split('/')
    chat_id = update.callback_query['message']['chat']['id']
    message_id = update.callback_query['message']['message_id']
    cur_user = update.callback_query.from_user
    try:
        username = cur_user.username
    except:
        username = ""
    try:
        last_name = cur_user.last_name
        name = cur_user.first_name + ' ' + last_name
    except:
        name = cur_user.first_name

    add_user(cur_user.id, username, name)

    if call_data[0] == 'pic':
        feedback_text = check_feedback(
            chat_id, message_id, cur_user.id, call_data[1])
        debug(
            bot, "[{}](tg://user?id={}) {} [this](https://t.me/{}/{}).".format(name, cur_user.id, '❤️' if call_data[1] == '1' else '😶', CHANNEL_PUBLICNAME, message_id))
        likes, dislikes = get_feedback(chat_id, message_id)
        bot.answer_callback_query(
            callback_query_id=update.callback_query.id, text=feedback_text)
        bot.edit_message_reply_markup(
            chat_id, message_id, reply_markup=like_buttons(likes, dislikes))
    elif call_data[0] == 'post':
        if call_data[1] == '1':
            file_id = update.callback_query['message']['reply_to_message']['photo'][-1]['file_id']
            caption = update.callback_query['message']['reply_to_message'].caption_markdown
            bot.answer_callback_query(
                callback_query_id=update.callback_query.id, text="正在发送/Sending~")
            sent_message = bot.send_photo(chat_id=CHANNEL, photo=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN,
                                          reply_markup=like_buttons(0, 0))['message_id']
            bot.edit_message_text("已发送。 Sent.", chat_id, message_id)
            debug(
                bot, "[{}](tg://user?id={}) sent [this](https://t.me/{}/{}).".format(name, cur_user.id, CHANNEL_PUBLICNAME, sent_message))
            init_message(chat_id, sent_message, cur_user.id)
            pic_id = add_picture(sent_message, file_id, caption)
            file = bot.get_file(file_id)
            file_name = "{}.jpg".format(pic_id)
            path = file_name
            file.download(path)
            with open(path, 'rb') as f:
                multipart_form_data = {
                    'file': (file_name, f),
                    'filename': (None, file_name),
                    'caption': (None, caption),
                    'token': (None, UPLOAD_TOKEN)
                }
                r = requests.post(UPLOAD_URL,
                                  files=multipart_form_data)
        else:
            bot.answer_callback_query(
                callback_query_id=update.callback_query.id, text="正在取消/Canceling~")
            bot.edit_message_text("已取消。 Canceled.", chat_id, message_id)
