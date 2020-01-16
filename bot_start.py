from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, ConversationHandler, CallbackQueryHandler ,PrefixHandler , JobQueue , Job
from telegram import ReplyKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardRemove
import datetime
import logging
import sqlite3

#bot_initialize
request_add,request_del,request_change,request_show,friends_show = 1,2,3,4,5

#logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#other
def database_execute(db_parse : str):
    try:
        db = sqlite3.connect("database.db")
        curs = db.cursor()
        curs.execute(db_parse)
        db.commit()
        db.close()
    except Exception:
        raise Exception

#bot_functionality

def bot_start(update,context):
    database_execute("""CREATE TABLE IF NOT EXISTS """ + 'table' + str(abs(update.effective_chat.id)) + """ (id TEXT PRIMARY KEY, day INT, month INT, year INT )""" )
    database_execute("""CREATE TABLE IF NOT EXISTS settings"""  + """ (tableid TEXT,  realid INT)""")
    database_execute("""INSERT INTO settings (tableid,realid) VALUES (""" + str(abs(update.effective_chat.id)) + "," + str(update.effective_chat.id) + ");")
    keys = [['>Show<','>Add<'],['>Change<','>Delete<']]
    context.bot.send_message(update.effective_chat.id, "Greetings! I am BIRTHDAY-bot. I'll help you with your amnesia. Choose option to proceed", reply_markup = ReplyKeyboardMarkup(keys,resize_keyboard= True))
    return ConversationHandler.END

def bot_add(update,context):
    context.bot.send_message(update.effective_chat.id, "To add your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo add you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can add multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000")
    return request_add

def bot_del(update,context):
    context.bot.send_message(update.effective_chat.id, "To delete your own birthday, simply type: 'me'.\nTo delete your friend's birthday, enter his username: @BFF.\nYou can delete multiple birthdays too: @BFF,@BFF")
    return request_del

def bot_change(update,context):
    context.bot.send_message(update.effective_chat.id, "To change your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo change you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can change multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000")
    return request_change

def bot_show(update,context):
    keys = [['>Current<','>Friends<','>All<']]
    context.bot.send_message(update.effective_chat.id, "Choose an option", reply_markup = ReplyKeyboardMarkup(keys, resize_keyboard = True))
    return request_show

def bot_show_friends(update,context):
    context.bot.send_message(update.effective_chat.id, "To see your own birthday, simply type: 'me'.\nTo see your friend's birthday, enter his username: @BFF.\nYou can see multiple birthdays too: @BFF,@BFF", reply_markup = ReplyKeyboardRemove())
    return friends_show

def bot_reminder(context):
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("""SELECT name FROM sqlite_master WHERE type='table'""") 
    db.commit()
    tables = list(curs)[:]
    del tables[-1]

    if len(tables) == 0:
        return None
 
    for table in tables:
        curs.execute("""SELECT id FROM """ + table[0] + """ WHERE day = """ + str(datetime.datetime.now().day) + """ AND month = """ + str(datetime.datetime.now().month))
        db.commit()
        lst_birthday = list(curs)[:]
        
        if len(lst_birthday) == 0:
            continue
        x = ""

        for users in lst_birthday:
            x += str(users[0]) + " "
        
        curs.execute("""SELECT realid FROM settings WHERE tableid = """ + table[0][5:])
        db.commit()

        realid = list(curs)[:]
        context.bot.send_message(realid[0][0],"Happy birthday to " + x)


# request_handling
def bot_request_add(update,context):
    try:
        lst_birthday = update.message.text.split('=')

        def check_date(lst_cut: list):
            if len(lst_cut) >= 4:
                raise Exception
            if not (lst_cut[0].isdigit() and lst_cut[1].isdigit() and  lst_cut[2].isdigit()):
                raise Exception
            if ((int(lst_cut[2]) < 0) or (1 > int(lst_cut[1]) or int(lst_cut[1])> 12) or (0 > int(lst_cut[0]) or int(lst_cut[0]) > 31)) or (int(lst_cut[1]) == 2 and int(lst_cut[0]) > 29):
                raise Exception
            return None   
        
        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].strip().split('.')
            check_date(lst_cut)
            database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'@""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            
        elif len(lst_birthday) == 2:
            lst_dates = lst_birthday[1].split(',')
            lst_usernames = lst_birthday[0].split(',')
            for user, date in zip(lst_usernames,lst_dates):
                lst_cut = date.strip().split('.')
                check_date(lst_cut)
                database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + ('@' if user[0] != '@' else '') + user.strip() + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
        else:
            raise Exception

        context.bot.send_message(update.effective_chat.id, "Thanks. I updated your birthday.")
        return ConversationHandler.END

    except Exception:
        context.bot.send_message(update.effective_chat.id, "Something went wrong!")
        return ConversationHandler.END

def bot_request_del(update,context):
    lst_birthday = update.message.text.split(',')
    for user in lst_birthday:
        if(user.strip().lower() == "me"):
            database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            if len(lst_birthday) == 1:
                context.bot.send_message(update.effective_chat.id, "Thanks. I deleted all mentioned entries of your friends birthday !")
                break      
        else:
            for admin in update.effective_chat.get_administrators():
                if(update.effective_user.id == admin.user.id):
                    database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') +user.strip() + """'""" + """;""")
                    context.bot.send_message(update.effective_chat.id, "Thanks. I deleted all mentioned entries of your friends birthday !")
                    break
            else:
                context.bot.send_message(update.effective_chat.id, "Sorry, but only administrators can delete other users")        
    return ConversationHandler.END

def bot_request_change(update,context):
    try:
        lst_birthday = update.message.text.split('=')

        def check_date(lst_cut: list):
            if len(lst_cut) >= 4:
                raise Exception
            if not (lst_cut[0].isdigit() and lst_cut[1].isdigit() and  lst_cut[2].isdigit()):
                raise Exception
            if ((int(lst_cut[2]) < 0) or (1 > int(lst_cut[1]) or int(lst_cut[1])> 12) or (1 > int(lst_cut[0]) or int(lst_cut[0]) > 31)) or (int(lst_cut[1]) == 2 and int(lst_cut[0]) > 29):
                raise Exception
            return None   
        
        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].strip().split('.')
            check_date(lst_cut)
            database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'@""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            
        elif len(lst_birthday) == 2:
            for admin in update.effective_chat.get_administrators():
                if(update.effective_user.id == admin.user.id):            
                    lst_dates = lst_birthday[1].split(',')
                    lst_usernames = lst_birthday[0].split(',')
                    for user, date in zip(lst_usernames,lst_dates):
                        lst_cut = date.strip().split('.')
                        check_date(lst_cut)
                        database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') + user.strip() + """'""" + """;""")
                        database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + ('@' if user[0] != '@' else '') +user.strip() + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
                    break
            else:
                context.bot.send_message(update.effective_chat.id, "Sorry, but only administrators can change other users")            
                return ConversationHandler.END
        else:
            raise Exception

        context.bot.send_message(update.effective_chat.id, "Thanks. I updated your birthday.")
        return ConversationHandler.END

    except Exception:
        context.bot.send_message(update.effective_chat.id, "Something went wrong! ")
        return ConversationHandler.END

def bot_show_all(update,context):
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("""SELECT * FROM table""" + str(abs(update.effective_chat.id)) + """ ORDER BY day,month""")
    db.commit()
    lst_birthday = list(curs)[:] 
    if len(lst_birthday) > 0:
        x = ""
        for row in lst_birthday:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
    else:
        x = "No birthdays in your database"

    context.bot.send_message(update.effective_chat.id,x, reply_markup = ReplyKeyboardMarkup([['>Show<','>Add<'],['>Change<','>Delete<']],resize_keyboard= True))
    return ConversationHandler.END

def bot_request_show_friends(update,context):
    lst_birthday = update.message.text.split(',')
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    lst_birth = list()

    for user in lst_birthday:
        x = ""
        if(user.strip().lower() == "me"):
            curs.execute("""SELECT * FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
        else:
            curs.execute("""SELECT * FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') + user + """'""" + """;""")
        db.commit()
        lst_birth += list(curs)[:]    
    else:
        for row in lst_birth:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
        context.bot.send_message(update.effective_chat.id, x if len(lst_birth) > 0 else "No match found!", reply_markup = ReplyKeyboardMarkup([['>Show<','>Add<'],['>Change<','>Delete<']],resize_keyboard= True))

    return ConversationHandler.END

def bot_show_current_month(update,context):
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("""SELECT * FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE month = """ + str(datetime.datetime.now().month))
    db.commit()
 
    lst_birthday = list(curs)[:] 
    if len(lst_birthday) > 0:
        x = ""
        for row in lst_birthday:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
    else:
        x = "No birthdays in this month"

    context.bot.send_message(update.effective_chat.id,x, reply_markup = ReplyKeyboardMarkup([['>Show<','>Add<'],['>Change<','>Delete<']],resize_keyboard= True))
    return ConversationHandler.END

def main():
    updater = Updater(token='YOUR TOKEN HERE', use_context=True)
    dispatcher = updater.dispatcher

    #bot_hadlers_creation
    bot_start_handler = ConversationHandler([CommandHandler('start',bot_start)],{},[])
    bot_add_handler = ConversationHandler([PrefixHandler('>','Add<',bot_add)],{request_add:[MessageHandler(Filters.text,bot_request_add)]},[])
    bot_del_handler = ConversationHandler([PrefixHandler('>','Delete<',bot_del)],{request_del:[MessageHandler(Filters.text,bot_request_del)]},[])
    bot_change_handler = ConversationHandler([PrefixHandler('>','Change<',bot_change)],{request_change:[MessageHandler(Filters.text,bot_request_change)]},[])
    bot_show_handler = ConversationHandler([PrefixHandler('>','Show<',bot_show)], {request_show:[PrefixHandler('>','All<',bot_show_all),PrefixHandler('>','Current<',bot_show_current_month),ConversationHandler([PrefixHandler('>','Friends<',bot_show_friends)],{friends_show:[MessageHandler(Filters.text,bot_request_show_friends)]},[],map_to_parent= {ConversationHandler.END : ConversationHandler.END })]},[])

    #bot_hadlers_registration
    dispatcher.add_handler(bot_start_handler)
    dispatcher.add_handler(bot_add_handler)
    dispatcher.add_handler(bot_del_handler)
    dispatcher.add_handler(bot_change_handler)
    dispatcher.add_handler(bot_show_handler)

    #Job
    Tasker = updater.job_queue
    Tasker.set_dispatcher(updater.dispatcher)
    Tasker.run_once(bot_reminder,2)


    #bot_start
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
