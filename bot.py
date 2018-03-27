import utils, commands, tasks, datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, CallbackQueryHandler
from creadcials import *

# Connect to the bot
updater = Updater(bot_token)

# Dispatch and add jobs
updater.dispatcher.add_handler(CommandHandler('start', commands.start))
updater.dispatcher.add_handler(CommandHandler('shota', commands.shota))
updater.dispatcher.add_handler(CommandHandler('help', commands.help))
updater.dispatcher.add_handler(CommandHandler('getin', commands.getin))
updater.dispatcher.add_handler(CommandHandler('hughug', commands.hughug))
updater.dispatcher.add_handler(CommandHandler('nick', commands.nick))
updater.dispatcher.add_handler(CommandHandler('list', commands.members))
updater.dispatcher.add_handler(CommandHandler('view', commands.cached_image))
updater.dispatcher.add_handler(CommandHandler('getid', commands.getid))
updater.dispatcher.add_handler(CommandHandler('bebug', commands.bebug))
updater.dispatcher.add_handler(CommandHandler('debug', commands.debug))

updater.job_queue.run_daily(tasks.daily_sch, time=datetime.time(0, 0, 0), name='daily')

updater.dispatcher.add_handler(CallbackQueryHandler(utils.callback_dispatcher))

# updater.dispatcher.add_handler(MessageHandler(Filters.all, utils.chat_dispatcher))

# Start the bot
updater.start_polling()
updater.idle()
