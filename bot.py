import utils
import commands
import datetime
import handlers
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from creadcials import BOT_TOKEN, PIXIV_PASSWORD, PIXIV_USERNAME

# Connect to the bot
UPDATER = Updater(BOT_TOKEN)

# Dispatch and add jobs
UPDATER.dispatcher.add_handler(CommandHandler('start', commands.start))
UPDATER.dispatcher.add_handler(CommandHandler('board', commands.contributors))

UPDATER.dispatcher.add_handler(MessageHandler(
    Filters.photo, handlers.photo_handler))
UPDATER.dispatcher.add_handler(MessageHandler(
    Filters.entity, handlers.entity_handler))
# Tasks
# updater.job_queue.run_daily(tasks.daily_sch, time=datetime.time(0, 0, 0), name='daily')

# Callback Button
UPDATER.dispatcher.add_handler(CallbackQueryHandler(utils.callback_dispatcher))

# Start the bot
UPDATER.start_polling()
UPDATER.idle()
