from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import os

updater = Updater(os.environ['API_KEY'],
                  use_context=True)


def oi(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello, Welcome to the Bot.Please write\
        /help to see the commands available.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /happy - Happy mood
    /food - Food
    /rom - Different command""")

updater.dispatcher.add_handler(CommandHandler('oi', oi))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.start_polling()
