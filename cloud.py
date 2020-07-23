from credentials import LEAN_APPKEY, LEAN_APPSEC
import leancloud
import logging

logging.basicConfig(level=logging.INFO)
leancloud.init(LEAN_APPKEY, LEAN_APPSEC)

leancloud.use_region('US')


def init_message(chat_id, message_id, from_user_id):
    feedback = [[], []]
    log_contributions(from_user_id, 1, "content")
    Message = leancloud.Object.extend('Message')
    message = Message()
    message.set('chat_id', chat_id)
    message.set('message_id', message_id)
    message.set('from', from_user_id)
    message.set('feedback', feedback)
    message.save()


def add_picture(message_id, file_id, caption):
    Picture = leancloud.Object.extend('Picture')
    pic = Picture()
    pic.set('message_id', message_id)
    pic.set('file_id', file_id)
    pic.set('caption', caption)
    pic.save()
    return pic.id


def check_feedback(chat_id, message_id, user_id, data):
    data = 1 if data == '1' else 0
    emoji = ['😶', '❤️']
    query_string = "select * from Message where message_id={} and chat_id={} limit 1".format(
        message_id, chat_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    text = 'You {} this message~'.format(emoji[data])
    if len(results):
        message = results[0]
        feedback = message.get('feedback')
        contrib = 0
        if user_id not in feedback[data]:
            feedback[data].append(user_id)
            contrib += 1
            if user_id in feedback[~data]:
                feedback[~data].remove(user_id)
                log_contributions(user_id, -1, "feedback")
                contrib -= 1
        else:
            feedback[data].remove(user_id)
            text = 'You took back your {}~'.format(emoji[data])
            contrib -= 1
        log_contributions(user_id, contrib, "feedback")
        message.set('feedback', feedback)
        message.save()
    else:
        feedback = [[], []]
        feedback[data].append(user_id)
        log_contributions(user_id, 1, "feedback")
        Message = leancloud.Object.extend('Message')
        message = Message()
        message.set('chat_id', chat_id)
        message.set('message_id', message_id)
        message.set('feedback', feedback)
        message.save()
    return text


def get_feedback(chat_id, message_id):
    query_string = "select * from Message where message_id={} and chat_id={} limit 1".format(
        message_id, chat_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    likes = dislikes = 0
    if len(results):
        feedback = results[0].get('feedback')
        likes = len(feedback[1])
        dislikes = len(feedback[0])
    return likes, dislikes


def log_contributions(user_id, value, TYPE="feedback"):
    weight = {
        'feedback': 1,
        'content': 5
    }
    user = get_user(user_id)
    contrib = user.get('user_contrib')
    user.set('user_contrib', value * weight[TYPE] + contrib)
    user.save()


def add_user(user_id, user_name, user_nick,):
    user = get_user(user_id)
    if (user):
        return user
    else:
        User = leancloud.Object.extend('Users')
        user = User()
        user.set('user_id', user_id)
        user.set('user_nick', user_nick)
        user.set('user_name', user_name)
        user.set('user_contrib', 0.0)
        user.save()
        return user


def if_blocked(user_id):
    query_string = "select * from Blacklist where id={} limit 1".format(
        user_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    if (len(results)):
        return True
    else:
        return None


def block_user(user_id):
    Hacker = leancloud.Object.extend('Blacklist')
    hacker = Hacker()
    hacker.set('id', user_id)
    hacker.save()


def get_user(user_id):
    query_string = "select * from Users where user_id={} limit 1".format(
        user_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    if (len(results)):
        return results[0]
    else:
        return None


def get_users():
    query_string = "select * from Users limit 10 order by user_contrib desc"
    return leancloud.Query.do_cloud_query(query_string).results
