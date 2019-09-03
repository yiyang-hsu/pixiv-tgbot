from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from pixivpy3 import AppPixivAPI
from creadcials import PIXIV_PASSWORD, PIXIV_USERNAME, OWNER


def debug(bot, obj):
    bot.send_message(chat_id=OWNER, text="`[status]` {}".format(obj),
                     disable_notification=True, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


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
    return build_menu([InlineKeyboardButton('是 / Yes', callback_data='post/1'),
                       InlineKeyboardButton('否 / No', callback_data='post/0')], n_cols=2)


def get_image_info(url: str):
    if ('pixiv' in url):
        api = AppPixivAPI()
        api.login(PIXIV_USERNAME, PIXIV_PASSWORD)
        if '?' in url:
            pixiv_id = int(dict(i.split('=')
                                for i in url.split('?')[-1].split('&'))['illust_id'])
        else:
            pixiv_id = int(url.split('/')[-1])
        return pixiv_download(pixiv_id, api)
    else:
        return {}


def pixiv_download(pixiv_id, api):
    if api.user_id == 0:
        api.login(PIXIV_USERNAME, PIXIV_USERNAME)
    json_result = api.illust_detail(pixiv_id, req_auth=True)
    if ('error' in json_result.keys()):
        return {}
    url_list = []
    count = json_result['illust']['page_count']
    if count == 1:
        url_list.append(
            json_result['illust']['meta_single_page']['original_image_url'])
    else:
        for i in range(count):
            url_list.append(
                json_result['illust']['meta_pages'][i]['image_urls']['original'])
    title = json_result['illust']['title']
    tags = json_result['illust']['tags']
    artist = json_result['illust']['user']['name']
    tags = [i['name'] for i in tags]

    files = []
    for url in url_list:
        name = url.split('/')[-1]
        local_url = '/tmp/' + name

        try:
            file = open(local_url, 'rb')
            files.append(local_url)
        except:
            api.download(url, path='/tmp/')
            files.append(local_url)

    return {'files': files, 'title': title, 'tags': tags, 'artist': artist, 'url': 'https://pixiv.net/i/{}'.format(pixiv_id)}
