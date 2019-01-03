import utils, commands, datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from creadcials import BOT_TOKEN

# Connect to the bot
UPDATER = Updater(BOT_TOKEN)

# Dispatch and add jobs
UPDATER.dispatcher.add_handler(CommandHandler('start', commands.start))
UPDATER.dispatcher.add_handler(CommandHandler('board', commands.contributors))

UPDATER.dispatcher.add_handler(MessageHandler(Filters.photo, utils.post_photos))
# Tasks
# updater.job_queue.run_daily(tasks.daily_sch, time=datetime.time(0, 0, 0), name='daily')

# Callback Button
UPDATER.dispatcher.add_handler(CallbackQueryHandler(utils.callback_dispatcher))

# Start the bot
UPDATER.start_polling()
UPDATER.idle()
