from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
import logging
import sqlite3

#bot_initialize
updater = Updater(token='YOUR TOKEN HERE', use_context=True)
dispatcher = updater.dispatcher

#logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#bot_functionality
def bot_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="hi, just write use /add_birthday to add your birthday")

def bot_unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="U try to hack me? 🖕")

def bot_new_member(update,context):
    for member in update.message.new_chat_members:
        if member.username == 'HB_chek_bot':
            def create_database_table():
                db = sqlite3.connect("birthday.db")
                curs = db.cursor()
                ident = "table" + str(-update.effective_chat.id)
                curs.execute("""CREATE TABLE IF NOT EXISTS """ + str(ident) + """ (id INT PRIMARY KEY, birthdat DATE)""")
            create_database_table()
            context.bot.send_message(chat_id=update.effective_chat.id, text="hi, just write /start to start work with me")
            break
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="hi, a new one, pls add your birthday /add_birthday 🤪")

def bot_add_birthday(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="enter u birthday date?\nYYYY-MM-DD")
    while(True):
        if update.message.from_user.id == update.effective_user.id:
            def check_date_valid():
                msg = update.message.

def bot_chat_kick(update,context):
    if update.message.left_chat_member.username == 'HB_chek_bot':
        def delete_database_table():
            db = sqlite3.connect("birthday.db")
            curs = db.cursor()
            ident = "table" + str(-update.effective_chat.id)
            curs.execute("""DROP TABLE """ + str(ident) + """;""")

#bot_hadlers_creation
start_handler = CommandHandler('start', bot_start)
new_member_handler = MessageHandler(Filters.status_update.new_chat_members,bot_new_member)
bot_chat_kick_handler = MessageHandler(Filters.status_update.left_chat_member,bot_chat_kick)
add_birthday_handler = CommandHandler('add_birthday',bot_add_birthday)
unknown_handler = MessageHandler(Filters.command, bot_unknown)

#bot_hadlers_registration
dispatcher.add_handler(start_handler)
dispatcher.add_handler(new_member_handler)
dispatcher.add_handler(bot_chat_kick_handler)
dispatcher.add_handler(add_birthday_handler)
dispatcher.add_handler(unknown_handler)

#bot_start
updater.start_polling()
updater.idle()
