from telegram import Bot, Update, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from cloud import get_feedback, check_feedback
from creadcials import CHANNEL


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu[0]


def post_photos(bot: Bot, update: Update):
    buttons = build_menu([InlineKeyboardButton('是', callback_data='post/1'),
                          InlineKeyboardButton('否', callback_data='post/0')], n_cols=2)

    message_id = update['message']['message_id']
    chat_id = update['message']['chat']['id']
    bot.send_message(chat_id=chat_id, text="您想要发送这张图片吗？", reply_to_message_id=message_id,
                     reply_markup=InlineKeyboardMarkup(buttons))


def like_buttons(likes, dislikes):
    return InlineKeyboardMarkup(build_menu([InlineKeyboardButton('❤️ {}'.format(str(likes)), callback_data='pic/1'), InlineKeyboardButton('😶 {}'.format(str(dislikes)), callback_data='pic/0')], n_cols=2))


def callback_dispatcher(bot: Bot, update: Update):
    call_data = update.callback_query['data'].split('/')
    chat_id = update.callback_query['message']['chat']['id']
    message_id = update.callback_query['message']['message_id']
    user_id = update.callback_query.from_user.id
    if call_data[0] == 'pic':
        feedback_text = check_feedback(
            chat_id, message_id, user_id, call_data[1])
        likes, dislikes = get_feedback(chat_id, message_id)
        bot.answer_callback_query(
            callback_query_id=update.callback_query.id, text=feedback_text)
        bot.edit_message_reply_markup(
            chat_id, message_id, reply_markup=like_buttons(likes, dislikes))
    elif call_data[0] == 'post':
        if call_data[1] == '1':
            file_id = update.callback_query['message']['reply_to_message']['photo'][-1]['file_id']
            caption = update.callback_query['message']['reply_to_message']['caption']
            bot.answer_callback_query(
                callback_query_id=update.callback_query.id, text="正在发送~")
            bot.send_photo(chat_id=CHANNEL, photo=file_id,
                           reply_markup=like_buttons(0, 0))
            bot.edit_message_text("已发送。", chat_id, message_id)
        else:
            bot.answer_callback_query(
                callback_query_id=update.callback_query.id, text="正在取消~")
            bot.edit_message_text("已取消。", chat_id, message_id)
