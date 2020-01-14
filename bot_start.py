from telegram.ext import Updater, CommandHandler,MessageHandler,Filters, ConversationHandler
import logging
import sqlite3

#bot_initialize
updater = Updater(token='910009672:AAEEvUKd4JcAmGMxjqxi0wtd0I3O_mzS9VM', use_context=True)
dispatcher = updater.dispatcher
POLL = 1

#logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#bot_functionality
def bot_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Драсте! Я ДН-БОТ_V1. Я запам'ятовую дати ваших народжень (якщо поможете) і нагадую Вам ,що ви на 1 рік ближче до 💀 .")

def bot_unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ти шо? Курча, мене зламати хочеш? Хуй тобі! 🖕")

def bot_new_member(update,context):
    for member in update.message.new_chat_members:
        if member.username == 'HB_chek_bot':
            def create_database_table():
                db = sqlite3.connect("birthday.db")
                curs = db.cursor()
                ident = "table" + str(abs(update.effective_chat.id))
                curs.execute("""CREATE TABLE IF NOT EXISTS """ + str(ident) + """ (id INT PRIMARY KEY, day INT, month INT, year INT)""")
            create_database_table()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Драсте! Я ДН-БОТ_V1. Я запам'ятовую дати ваших народжень (якщо поможете) і нагадую вам ,що ви на 1 рік ближче до 💀 . Для початку роботи зі мною пропишіть /start")
            break
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Я бачу у вас тут новий ПІДОР. Ну здарасте, здрасте. Я ДН-БОТ. Не забудь добавити мені свою дату народження. ОК? Бо заріжу 🤪")

def bot_add_birthday(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Коли ж ти народився, а?\nВведи дату в такому форматі DD.MM.YYYY")
    return POLL

def bot_chat_poll(update,context):
    msg = update.effective_message.text
    msg = msg.split('.')
    print(msg)
    def insert_database_table():
        db = sqlite3.connect("birthday.db")
        curs = db.cursor()
        user_id = str(abs(update.effective_user.id))
        ident = "table" + str(abs(update.effective_chat.id))
        curs.execute("""INSERT INTO """ + str(ident) + """ (id, day, month, year) VALUES ("""  + user_id +  ""","""  + msg[0] + """,""" + msg[1] + """,""" + msg[2] + """)""")
        db.commit()
    insert_database_table()
    return ConversationHandler.END

def bot_add_birthday_cancel(update,context):
    return ConversationHandler.END

def bot_chat_kick(update,context):
    print("DELETED")
    if update.message.left_chat_member.username == 'HB_chek_bot':
        def delete_database_table():
            db = sqlite3.connect("birthday.db")
            curs = db.cursor()
            ident = "table" + str(abs(update.effective_chat.id))
            curs.execute("""DROP TABLE """ + str(ident) + """;""")
        delete_database_table()

#bot_hadlers_creation
new_member_handler = MessageHandler(Filters.status_update.new_chat_members,bot_new_member)
bot_chat_kick_handler = MessageHandler(Filters.status_update.left_chat_member,bot_chat_kick)
start_handler = CommandHandler('start', bot_start)
add_birthday_handler = ConversationHandler(entry_points = [CommandHandler('add_birthday',bot_add_birthday)], states = {POLL: [MessageHandler(Filters.text,bot_chat_poll)]}, fallbacks = [CommandHandler('cancel',bot_add_birthday_cancel)])
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
