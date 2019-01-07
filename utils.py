from telegram import Bot, Update, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from cloud import get_feedback, check_feedback, add_user, log_contributions
from creadcials import CHANNEL, PIXIV_PASSWORD, PIXIV_USERNAME
from pixivpy3 import AppPixivAPI


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


def like_buttons(likes, dislikes):
    return InlineKeyboardMarkup(build_menu([InlineKeyboardButton('❤️ {}'.format(str(likes)), callback_data='pic/1'), InlineKeyboardButton('😶 {}'.format(str(dislikes)), callback_data='pic/0')], n_cols=2))


def confirm_buttons():
    return build_menu([InlineKeyboardButton('是', callback_data='post/1'),
                       InlineKeyboardButton('否', callback_data='post/0')], n_cols=2)


def callback_dispatcher(bot: Bot, update: Update):
    call_data = update.callback_query['data'].split('/')
    chat_id = update.callback_query['message']['chat']['id']
    message_id = update.callback_query['message']['message_id']
    cur_user = update.callback_query.from_user
    add_user(cur_user.id, cur_user.username,
             cur_user.first_name + ' ' + cur_user.last_name)
    if call_data[0] == 'pic':
        feedback_text = check_feedback(
            chat_id, message_id, cur_user.id, call_data[1])
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
            bot.send_photo(chat_id=CHANNEL, photo=file_id, caption=caption,
                           reply_markup=like_buttons(0, 0))
            bot.edit_message_text("已发送。", chat_id, message_id)
            log_contributions(cur_user.id, 1, 'content')
        else:
            bot.answer_callback_query(
                callback_query_id=update.callback_query.id, text="正在取消~")
            bot.edit_message_text("已取消。", chat_id, message_id)


def get_image_info(url: str):

    if (url.startswith('https://www.pixiv') or url.startswith('https://i.pixiv') or url.startswith('https://pixiv')):
        api = AppPixivAPI()
        api.login(PIXIV_USERNAME, PIXIV_PASSWORD)
        return pixiv_download(int(url.split('=')[-1]), api)


def pixiv_download(pixiv_id, api):
    if api.user_id == 0:
        api.login(PIXIV_USERNAME, PIXIV_USERNAME)
    json_result = api.illust_detail(pixiv_id, req_auth=True)
    if ('error' in json_result.keys()):
        local_url = -1
        title = -1
        tag = -1
        file = -1
        artist = - 1
    else:
        if json_result['illust']['page_count'] == 1:
            url = json_result['illust']['meta_single_page']['original_image_url']
        else:
            url = json_result['illust']['meta_pages'][0]['image_urls']['original']
        title = json_result['illust']['title']
        tags = json_result['illust']['tags']
        artist = json_result['illust']['user']['name']
        tags = [i['name'] for i in tags]

        name = url.split('/')[-1]
        local_url = '/tmp/' + name

        try:
            file = open(local_url, 'rb')
            file = local_url
        except:
            api.download(url, path='/tmp/')
            file = local_url

    return file, title, tags, artist
