import commands, subprocess, requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import telegram
import random
import sqlite3

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

def get_image_info():
    url = 'https://image.benzishe.net/?random'
    cookies = dict(AGREE_CONSENT='1')
    try:
        html_res = requests.get(url, cookies = cookies)
    except: 
        return 0
    view_url = html_res.url
    html_text = html_res.text
    parsed_html = BeautifulSoup(html_text, 'lxml')
    image_url = parsed_html.head.find('link', attrs={'rel':'image_src'})
    image_up = parsed_html.body.find('a', attrs={'rel':'author'})
    views_count = parsed_html.body.find('div', attrs={'class':'number-figures'}).text.split('次')[0]
    likes_count = parsed_html.body.find('b', attrs={'data-text':'likes-count'}).text
    image_info = dict({
        'image_url': image_url['href'],
        'view_url': view_url,
        'up_name': image_up.text,
        'up_link': image_up['href'],
        'views': views_count,
        'likes': likes_count,
    })
    row_id = update_image(image_info)
    image_info['row_id'] = row_id
    return image_info

def callback_dispatcher(bot, update):
    call_str = update.callback_query['data'].split('/')
    chat_id = update.callback_query['message']['chat']['id']
    message_id = update.callback_query['message']['message_id']
    click_userid = str(update.callback_query.from_user.id)
    add_new_user(update.callback_query.from_user)
    if call_str[0] == 'hug':
        userid = str(update.callback_query['message']['reply_to_message'].from_user.id)
        if (click_userid != userid):
            bot.answer_callback_query(callback_query_id=update.callback_query.id, text='不是你发的命令喔~')
            return
        user_dict = get_user_list('dict')
        choice = int(random.getrandbits(3))
        text1 = '😝{name}让你抱抱了！'
        text0 = '😏{name}才不要你抱抱！'
        if(userid == call_str[1]):
            bot.answer_callback_query(callback_query_id=update.callback_query.id, text='抱抱成功！')
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='😶{name}心疼地抱了抱自己。'.format(name = user_dict[call_str[1]]['alias'] if user_dict[call_str[1]]['alias'] else user_dict[call_str[1]]['first_name']))
        elif (userid == '455677368'):
            bot.answer_callback_query(callback_query_id=update.callback_query.id, text='抱抱成功！')
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text1.format(name=user_dict[call_str[1]]['alias'] if user_dict[call_str[1]]['alias'] else user_dict[call_str[1]]['first_name']))
        else:
            if (choice<=user_dict[call_str[1]]['index']):
                bot.answer_callback_query(callback_query_id=update.callback_query.id, text='抱抱成功！')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text1.format(name=user_dict[call_str[1]]['alias'] if user_dict[call_str[1]]['alias'] else user_dict[call_str[1]]['first_name']))
            else:
                bot.answer_callback_query(callback_query_id=update.callback_query.id, text='抱抱失败！')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text0.format(name=user_dict[call_str[1]]['alias'] if user_dict[call_str[1]]['alias'] else user_dict[call_str[1]]['first_name']))
    elif call_str[0] == 'view':
        view_handler(bot, update, chat_id, message_id, call_str[1])
        return

def hug_handler(bot, update, chat_id, message_id, userid):
    return

def view_handler(bot, update, chat_id, message_id, value):
    if (value == 'del'):
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        return
    rowid = int(value)
    values = format_view_reply(rowid)
    if (values[0]):
        bot.answer_callback_query(callback_query_id=update.callback_query.id, text='第'+ str(rowid) + '张~')
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=values[0], reply_markup=values[1],parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.answer_callback_query(callback_query_id=update.callback_query.id, text='没有了~')
    return


def get_user_list(data):
    conn = sqlite3.connect('./tgbzs.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * from userinfo")
    values = cursor.fetchall()
    if (data == 'list'):
        user_list = []
        for item in values:
            user_list.append({
                'userid': item[0],
                'alias': item[1],
                'first_name': item[2],
                'last_name': item[3],
                'index': item[4]
            })
    elif (data == 'dict'):
        user_list = dict()
        for item in values:
            user_list[item[0]] = {
                'alias': item[1],
                'first_name': item[2],
                'last_name': item[3],
                'index': item[4]
            }
    return user_list

def add_new_user(from_user):
    conn = sqlite3.connect('./tgbzs.db')
    c = conn.cursor()
    try:
        cursor = c.execute("SELECT * from userinfo where userid = {userid}".format(userid = from_user.id))
        values = cursor.fetchall()
    except:
        values = NULL
        pass
    if (not values):
        try:
            c.execute("insert into userinfo (userid, first_name, last_name, 'index') VALUES ('{id}','{first_name}', '{last_name}', 4)".format(id = from_user.id, first_name = from_user.first_name, last_name = from_user.last_name))
            conn.commit()
        except:
            pass
    return

def update_nick(from_user, nick_name):
    add_new_user(from_user)
    conn = sqlite3.connect('./tgbzs.db')
    c = conn.cursor()
    try:
        c.execute("update userinfo set alias = '{nick_name}' where userid = '{id}'".format(nick_name = nick_name, id = from_user.id))
        conn.commit()
    except:
        pass
    return

def update_image(image_info):
    conn = sqlite3.connect('./tgbzs.db')
    c = conn.cursor()
    try:
        cursor = c.execute("SELECT * from image where view_url = '{url}'".format(url = image_info['view_url']))
        values = cursor.fetchall()
    except:
        values = NULL
        pass
    if (not values):
        try:
            c.execute("insert into image (image_url, view_url, up_name, up_link, likes, views) VALUES ('{image_url}', '{view_url}', '{up_name}', '{up_link}', {likes}, {views})".format(image_url = image_info['image_url'], view_url = image_info['view_url'], up_name = image_info['up_name'], up_link = image_info['up_link'], likes = image_info['likes'], views = image_info['views']))
            conn.commit()
        except:
            pass
    else:
        try:
            c.execute("update image set likes = {likes}, set views = {views} where view_url = '{view_url}'".format(view_url = image_info['view_url'], likes = image_info['likes'], views = image_info['views']))
            conn.commit()
        except:
            pass
    sql = "select rowid from image where view_url = '{url}'".format(url = image_info['view_url'])
    cursor = c.execute(sql)
    values = cursor.fetchall()
    return values[0][0]

def get_image(rowid):
    conn = sqlite3.connect('./tgbzs.db')
    c = conn.cursor()
    image_info = {}
    sql = "select * from image where rowid = {rowid}".format(rowid = rowid)
    try:
        cursor = c.execute(sql)
        values = cursor.fetchall()
    except:
        values = NULL
        pass
    if (values):
        item = values[0]
        image_info = {
                'image_url': item[0],
                'view_url': item[1],
                'up_name': item[2],
                'up_link': item[3],
                'likes': item[4],
                'views': item[5],
                'row_id': rowid
            }
        return image_info
    else:
        return 0 

def format_view_reply(rowid):
    image_info = get_image(rowid)
    if (not image_info):
        return ('', '')
    text = format_shota_reply(image_info)
    button_list = [telegram.InlineKeyboardButton('上一张', callback_data='view/' + str(rowid-1)),
                   telegram.InlineKeyboardButton('查看', url=image_info['view_url']),
                   telegram.InlineKeyboardButton('下一张', callback_data='view/' + str(rowid+1)),
                   telegram.InlineKeyboardButton('关闭浏览', callback_data='view/' + 'del')]
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    return (text, reply_markup)

def format_shota_reply(image_info):
    text = "*No. {rowid} *| [Image]({image_url}) | [Link]({view_url})\n------------\nUploaded by [{up_name}]({up_link})\n查看: {views}\n喜欢: {likes}".format(
            rowid = image_info['row_id'],
            view_url = image_info['view_url'],
            image_url = image_info['image_url'],
            up_name = image_info['up_name'],
            up_link = image_info['up_link'],
            views = image_info['views'],
            likes = image_info['likes']
        )
    return text
