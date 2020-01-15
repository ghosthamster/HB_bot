from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, ConversationHandler, CallbackQueryHandler ,PrefixHandler
from telegram import ReplyKeyboardMarkup, CallbackQuery, KeyboardButton
import logging
import sqlite3

#bot_initialize
request_add,request_del,request_change = 1,2,3

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
    database_execute("""CREATE TABLE IF NOT EXISTS """ + 'table' + str(abs(update.effective_chat.id)) + """ (id TEXT PRIMARY KEY, day INT, month INT, year INT)""" )
    keys = [['>Show<','>Add<'],['>Change<','>Delete<']]
    context.bot.send_message(update.effective_chat.id, "Greetings! I am BIRTHDAY-bot. I'll help you with your amnesia. Choose option to proceed", reply_markup = ReplyKeyboardMarkup(keys,resize_keyboard= True))

def bot_add(update,context):
    context.bot.send_message(update.effective_chat.id, "To add your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo add you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can add multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000")
    return request_add

def bot_del(update,context):
    context.bot.send_message(update.effective_chat.id, "To delete your own birthday, simply type: 'me'.\nTo delete your friend's birthday, enter his username: @BFF.\nYou can delete multiple birthdays too: @BFF,@BFF")
    return request_del

def bot_change(update,context):
    context.bot.send_message(update.effective_chat.id, "To change your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo change you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can change multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000")
    return request_change

#request_handling
def bot_request_add(update,context):
    try:
        lst_birthday = update.message.text.split('=')

        def check_date(lst_cut: list):
            if len(lst_cut) >= 4:
                raise Exception
            if not (lst_cut[0].isdigit() and lst_cut[1].isdigit() and  lst_cut[2].isdigit()):
                raise Exception
            if ((int(lst_cut[2]) < 0) or (0 > int(lst_cut[1]) or int(lst_cut[1])> 13) or (0 > int(lst_cut[0]) or int(lst_cut[0]) > 32)) or (int(lst_cut[1]) == 2 and int(lst_cut[0]) > 29):
                raise Exception
            return None   
        
        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].split('.')
            check_date(lst_cut)
            database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'@""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            
        elif len(lst_birthday) == 2:
            lst_dates = lst_birthday[1].split(',')
            lst_usernames = lst_birthday[0].split(',')
            for user, date in zip(lst_usernames,lst_dates):
                lst_cut = date.split('.')
                check_date(lst_cut)
                database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + user + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
        else:
            raise Exception

        context.bot.send_message(update.effective_chat.id, "Thanks. I updated your birthday.")
        return ConversationHandler.END

    except Exception:
        context.bot.send_message(update.effective_chat.id, "Something went wrong!")
        return request_add


def bot_request_del(update,context):
    lst_birthday = update.message.text.split(',')
    print(lst_birthday)
    for user in lst_birthday:
        if(user.strip() == "me"):
            database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            if len(lst_birthday) == 1:
                context.bot.send_message(update.effective_chat.id, "Thanks. I deleted all mentioned entries of your friends birthday !")
                break      
        else:
            for admin in update.effective_chat.get_administrators():
                if(update.effective_user.id == admin.user.id):
                    database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + user + """'""" + """;""")
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
            if ((int(lst_cut[2]) < 0) or (0 > int(lst_cut[1]) or int(lst_cut[1])> 13) or (0 > int(lst_cut[0]) or int(lst_cut[0]) > 32)) or (int(lst_cut[1]) == 2 and int(lst_cut[0]) > 29):
                raise Exception
            return None   
        
        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].split('.')
            check_date(lst_cut)
            database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            
        elif len(lst_birthday) == 2:
            for admin in update.effective_chat.get_administrators():
                if(update.effective_user.id == admin.user.id):            
                    lst_dates = lst_birthday[1].split(',')
                    lst_usernames = lst_birthday[0].split(',')
                    for user, date in zip(lst_usernames,lst_dates):
                        lst_cut = date.split('.')
                        check_date(lst_cut)
                        database_execute("""DELETE FROM table""" + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + user + """'""" + """;""")
                        database_execute("""INSERT INTO table""" + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + user + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
                    break
            else:
                context.bot.send_message(update.effective_chat.id, "Sorry, but only administrators can change other users")            
                return ConversationHandler.END
        else:
            raise Exception

        context.bot.send_message(update.effective_chat.id, "Thanks. I updated your birthday.")
        return ConversationHandler.END

    except Exception:
        context.bot.send_message(update.effective_chat.id, "Something went wrong!")
        return request_add


def main():
    updater = Updater(token='YOUR TOKEN HERE', use_context=True)
    dispatcher = updater.dispatcher

    #bot_hadlers_creation
    bot_start_handler = CommandHandler('start',bot_start)
    bot_add_handler = ConversationHandler([PrefixHandler('>','Add<',bot_add)],{request_add:[MessageHandler(Filters.text,bot_request_add)]},[])
    bot_del_handler = ConversationHandler([PrefixHandler('>','Delete<',bot_del)],{request_del:[MessageHandler(Filters.text,bot_request_del)]},[])
    bot_change_handler = ConversationHandler([PrefixHandler('>','Change<',bot_change)],{request_change:[MessageHandler(Filters.text,bot_request_change)]},[])

    #bot_hadlers_registration
    dispatcher.add_handler(bot_start_handler)
    dispatcher.add_handler(bot_add_handler)
    dispatcher.add_handler(bot_del_handler)
    dispatcher.add_handler(bot_change_handler)

    #bot_start
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
