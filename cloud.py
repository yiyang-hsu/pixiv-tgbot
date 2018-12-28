from creadcials import LEAN_APPKEY, LEAN_APPSEC
import leancloud
import logging

logging.basicConfig(level=logging.DEBUG)


leancloud.init(LEAN_APPKEY, LEAN_APPSEC)

print(LEAN_APPKEY)
print(LEAN_APPSEC)

leancloud.use_region('US')

def check_feedback(chat_id, message_id, user_id, data):
    data = 1 if data == '1' else 0
    emoji = ['😶', '❤️']
    query_string = "select * from Message where message_id={} and chat_id={} limit 1".format(message_id, chat_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    text = 'You {} this message~'.format(emoji[data])
    if len(results):
        message = results[0]
        feedback = message.get('feedback')
        if user_id not in feedback[data]:
            feedback[data].append(user_id)
            if user_id in feedback[~data]:
                feedback[~data].remove(user_id)
        else:
            feedback[data].remove(user_id)
            text = 'You took back your {}~'.format(emoji[data])
        message.set('feedback', feedback)
        message.save()
    else:
        feedback = [[], []]
        feedback[data].append(user_id)
        Message = leancloud.Object.extend('Message')
        message = Message()
        message.set('chat_id', chat_id)
        message.set('message_id', message_id)
        message.set('feedback', feedback)
        message.save()
    return text

def get_feedback(chat_id, message_id):
    query_string = "select * from Message where message_id={} and chat_id={} limit 1".format(message_id, chat_id)
    results = leancloud.Query.do_cloud_query(query_string).results
    likes = dislikes = 0
    if len(results):
        feedback = results[0].get('feedback')
        likes = len(feedback[1])
        dislikes = len(feedback[0])
    return likes, dislikes
