from telegram.ext import Updater, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, ParseMode
from bot_replies import *
import datetime
import time
import random
import logging
import sqlite3

#---------[bot_initialize]---------
request_add,request_del,request_change,request_show,friends_show,request_settings,feedback_request,custom_wishes_request,request_add_wish = 1,2,3,4,5,6,7,8,9
logging.basicConfig(filename= "logs.log",level=logging.INFO)


#---------[bot_functionality]---------
def bot_start(update,context):
    database_execute("""CREATE TABLE IF NOT EXISTS table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id TEXT PRIMARY KEY, day INT, month INT, year INT )""" )
    database_execute("""CREATE TABLE IF NOT EXISTS settings"""  + """ (tableid TEXT PRIMARY KEY,  realid INT, defaultBirthday BIT, customWishes TEXT )""")
    database_execute("""INSERT OR IGNORE INTO settings (tableid,realid,defaultBirthday,customWishes) VALUES ('""" + ("C" if update.effective_chat.id < 0 else "") + str(abs(update.effective_chat.id)) + "'," + str(update.effective_chat.id) +", 0,'');")
    update.message.reply_text(bot_reply[start], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard = True,selective= True, one_time_keyboard= True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

def bot_add(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[add], parse_mode = ParseMode.MARKDOWN)
    return request_add

def bot_del(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[delete] , parse_mode = ParseMode.MARKDOWN)
    return request_del

def bot_change(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[change] , parse_mode = ParseMode.MARKDOWN)
    return request_change

def bot_show(update,context):
    update.message.reply_text(bot_reply[show] , reply_markup = ReplyKeyboardMarkup(bot_keyboard[show_menu], resize_keyboard = True,selective= True,one_time_keyboard= True), parse_mode = ParseMode.MARKDOWN)
    return request_show

def bot_show_friends(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[show_friends] , parse_mode = ParseMode.MARKDOWN)
    return friends_show

def bot_settings(update,context):
    update.message.reply_text(bot_reply[show], reply_markup = ReplyKeyboardMarkup(bot_keyboard[settings_menu],resize_keyboard=True,one_time_keyboard=True,selective=True), parse_mode = ParseMode.MARKDOWN)
    return request_settings

def bot_feedback(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[feedback], parse_mode = ParseMode.MARKDOWN)
    return feedback_request

def bot_custom_wishes(update,context):
    update.message.reply_text(bot_reply[show], parse_mode = ParseMode.MARKDOWN, reply_markup = ReplyKeyboardMarkup(bot_keyboard[custom_wishes],resize_keyboard=True,one_time_keyboard=True,selective=True))
    return custom_wishes_request

def bot_add_wish(update,context):
    context.bot.send_message(update.effective_chat.id, bot_reply[add_wish], parse_mode = ParseMode.MARKDOWN)
    return request_add_wish

def bot_delete_wishes(update,context):
    database_execute("""UPDATE settings SET customWishes = '' WHERE tableid = '"""  + ("C" if update.effective_chat.id < 0 else "") + str(abs(update.effective_chat.id)) + """';""")
    update.message.reply_text(bot_reply[delete_wishes], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END 

def bot_left_chat(update,context):
    if update.effective_message.left_chat_member.id == context.bot.id:
        database_execute("""DELETE FROM settings WHERE tableid = '"""  + ('C' if update.effective_chat.id < 0 else '') +  str(abs(update.effective_chat.id)) + """';""")
        database_execute("""DROP TABLE table""" + ('C' if update.effective_chat.id < 0 else '') +str(abs(update.effective_chat.id)))    

def bot_reminder(context):
    tables = list()
    default = list()
    database_execute("""SELECT name FROM sqlite_master WHERE type='table'""", tables)
    tables.remove(('settings',))

    if len(tables) == 0:
        return None
    
    for table in tables:
        lst_birthday = list()
        database_execute("""SELECT id FROM """ + table[0] + """ WHERE day = """ + str(datetime.datetime.now().day) + """ AND month = """ + str(datetime.datetime.now().month),lst_birthday)
        database_execute("""SELECT defaultBirthday FROM settings WHERE tableid = '""" + table[0][5:] + """';""",default)
        
        if len(lst_birthday) == 0:
            continue
        x = ""

        for users in lst_birthday:
            x += str(users[0]) + " "
        
        if(table[0][5].isdigit()):
            context.bot.send_message(int(table[0][5:]) if table[0][5].isdigit() else -(int(table[0][6:])) ,"* DONT FORGET: * _ today _ {0} _ were born. So wish them all the best! _".format(x), parse_mode = ParseMode.MARKDOWN)
        else:
            random.seed(time.time())
            if default[0][0] == 1:
                context.bot.send_message(int(table[0][5:]) if table[0][5].isdigit() else -(int(table[0][6:])) ,bot_birthday_msg[random.randint(0,len(bot_birthday_msg) - 1)].format(x), parse_mode = ParseMode.MARKDOWN)
            else:
                database_execute("""SELECT customWishes FROM settings WHERE tableid = '""" + table[0][5:] + """';""",default)
                lst_customWishes = default[1][0].split("###")
                context.bot.send_message(int(table[0][5:]) if table[0][5].isdigit() else -(int(table[0][6:])) ,lst_customWishes[random.randint(0,len(lst_customWishes) - 2)].format(x), parse_mode = ParseMode.MARKDOWN)

#---------[request_handling]---------
def bot_request_add(update,context):
    try:
        already_in = str()
        lst_birthday = update.message.text.split('=')
        
        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].strip().split('.')
            check_date(lst_cut)
            try:
                database_execute("""INSERT INTO table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'@""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            except database_exeption:
                already_in += '@' + update.effective_user.username
        elif len(lst_birthday) == 2:
            lst_dates = lst_birthday[1].split(',')
            lst_usernames = lst_birthday[0].split(',')
            for user, date in zip(lst_usernames,lst_dates):
                lst_cut = date.strip().split('.')
                check_date(lst_cut)
                try:
                    database_execute("""INSERT INTO table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + ('@' if user[0] != '@' else '') + user.strip() + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
                except database_exeption:
                    already_in += user + ' '
        else:
            raise birthday_WrongFormat_exception
        context.bot.send_message(update.effective_chat.id, bot_reply[add_request] + (str(bot_reply[sql_already_in] + already_in) if len(already_in) else '') ,parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END

    except birthday_WrongFormat_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[wrong_format], parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END
    except birthday_WrongDate_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[wrong_date] ,parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END
    except birthday_NotDate_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[not_a_date] , parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END

def bot_request_del(update,context):
    lst_birthday = update.message.text.split(',')
    for user in lst_birthday:
        if(user.strip().lower() == "me"):
            database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            if len(lst_birthday) == 1:
                break      
        else:
            if(update.effective_chat.id < 0):
                for admin in update.effective_chat.get_administrators():
                    if(update.effective_user.id == admin.user.id):
                        database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0].strip() != '@' else '') + user.strip() + """'""" + """;""")
                        break
                else:
                    context.bot.send_message(update.effective_chat.id, bot_reply[not_admin], parse_mode = ParseMode.MARKDOWN)
                    return ConversationHandler.END
            else:
                database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0].strip() != '@' else '') + user.strip() + """'""" + """;""")
                break

    context.bot.send_message(update.effective_chat.id, bot_reply[delete_request], parse_mode = ParseMode.MARKDOWN)        
    return ConversationHandler.END

def bot_request_change(update,context):
    try:
        lst_birthday = update.message.text.split('=')

        if len(lst_birthday) == 1:
            lst_cut = lst_birthday[0].strip().split('.')
            check_date(lst_cut)
            database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""")
            database_execute("""INSERT INTO table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'@""" + update.effective_user.username + """'"""  + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
            
        elif len(lst_birthday) == 2:
            lst_dates = lst_birthday[1].split(',')
            lst_usernames = lst_birthday[0].split(',')

            if(update.effective_chat.id < 0): 
                for admin in update.effective_chat.get_administrators():
                    if(update.effective_user.id == admin.user.id):            
                        for user, date in zip(lst_usernames,lst_dates):
                            lst_cut = date.strip().split('.')
                            check_date(lst_cut)
                            database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') + user.strip() + """'""" + """;""")
                            database_execute("""INSERT INTO table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + ('@' if user[0] != '@' else '') +user.strip() + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
                        break
                else:
                    context.bot.send_message(update.effective_chat.id, bot_reply[not_admin], parse_mode = ParseMode.MARKDOWN)            
                    return ConversationHandler.END
            else:
                for user, date in zip(lst_usernames,lst_dates):
                    lst_cut = date.strip().split('.')
                    check_date(lst_cut)
                    database_execute("""DELETE FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') + user.strip() + """'""" + """;""")
                    database_execute("""INSERT INTO table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ (id,day,month,YEAR) VALUES (""" + """'""" + ('@' if user[0] != '@' else '') +user.strip() + """'""" + "," + lst_cut[0] + "," + lst_cut[1] + "," + lst_cut[2] + """);""")
                    break                    
        else:
            raise birthday_WrongFormat_exception

        context.bot.send_message(update.effective_chat.id, bot_reply[change_request], parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END

    except birthday_WrongFormat_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[wrong_format] ,parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END
    except birthday_WrongDate_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[wrong_date] , parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END
    except birthday_NotDate_exception:
        context.bot.send_message(update.effective_chat.id, bot_reply[not_a_date] ,parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END

def bot_show_all(update,context):
    lst_birthday = list()
    database_execute("""SELECT * FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ ORDER BY day,month""",lst_birthday) 
    
    if len(lst_birthday) > 0:
        x = ""
        for row in lst_birthday:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
    else:
        x = bot_reply[empty_database]

    update.message.reply_text(x, reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True, one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

def bot_request_show_friends(update,context):
    lst_birthday = update.message.text.split(',')
    lst_birth = list()

    for user in lst_birthday:
        x = ""
        if(user.strip().lower() == "me"):
            database_execute("""SELECT * FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'@""" + update.effective_user.username + """'""" + """;""",lst_birth)
        else:
            database_execute("""SELECT * FROM table""" + ('C' if update.effective_chat.id < 0 else '') +str(abs(update.effective_chat.id)) + """ WHERE id = """ + """'""" + ('@' if user[0] != '@' else '') + user + """'""" + """;""",lst_birth)   
    else:
        for row in lst_birth:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
        update.message.reply_text(x if len(lst_birth) > 0 else bot_reply[empty_request], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)

    return ConversationHandler.END

def bot_show_current_month(update,context):
    lst_birthday = list() 
    database_execute("""SELECT * FROM table""" + ('C' if update.effective_chat.id < 0 else '') + str(abs(update.effective_chat.id)) + """ WHERE month = """ + str(datetime.datetime.now().month),lst_birthday)

    if len(lst_birthday) > 0:
        x = ""
        for row in lst_birthday:
            user = "User: " + str(row[0])
            birthday = "Birthday: " + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) +"\n"
            x = x + "{0:<20}\n{1:<20}\n".format(user,birthday)
    else:
        x = bot_reply[empty_month]

    update.message.reply_text(x, reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

def bot_cancel(update,context):
    update.message.reply_text(bot_reply[cancel], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

def bot_feedback_request(update,context):
    msg = update.effective_message
    context.bot.send_message(272151950,"FEEDBACK of " + str(msg.from_user.id) + " : " + msg.text)
    context.bot.send_message(660560081,"FEEDBACK of " + str(msg.from_user.id) + " : " + msg.text)
    update.message.reply_text(bot_reply[feedback_req],parse_mode = ParseMode.MARKDOWN, reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True))
    return ConversationHandler.END

def bot_custom_wishes_request(update,context):
    if "❌OFF❌" == update.effective_message.text:
        database_execute("""UPDATE settings SET defaultBirthday = 1 WHERE tableid = '""" + ("C" if update.effective_chat.id < 0 else "") + str(abs(update.effective_chat.id)) + """';""")
    elif "✅ON✅" == update.effective_message.text:
        database_execute("""UPDATE settings SET defaultBirthday = 0 WHERE tableid = '""" + ("C" if update.effective_chat.id < 0 else "") + str(abs(update.effective_chat.id)) + """';""")
    else:
        update.message.reply_text(bot_reply[wrong_input], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    update.message.reply_text(bot_reply[custom_wishes_req], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

def bot_add_wish_request(update,context):
    wishes_list = update.effective_message.text.split("###")
    for wish in wishes_list:
        if wish.find("{0}") == -1:
            update.message.reply_text(bot_reply[missed_sym], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
            return ConversationHandler.END
    database_execute("""UPDATE settings SET customWishes = customWishes || '""" + update.effective_message.text.strip() + """###' WHERE tableid = """ + """'""" + ("C" if update.effective_chat.id < 0 else "") + str(abs(update.effective_chat.id)) + """';""")
    update.message.reply_text(bot_reply[add_wish_request], reply_markup = ReplyKeyboardMarkup(bot_keyboard[main_menu],resize_keyboard= True,selective= True,one_time_keyboard = True),parse_mode = ParseMode.MARKDOWN)
    return ConversationHandler.END

#---------[other]--------- 

def check_date(lst_cut: list):
    if len(lst_cut) >= 4 or len(lst_cut) < 3:
        raise birthday_WrongFormat_exception
    if not (lst_cut[0].isdigit() and lst_cut[1].isdigit() and  lst_cut[2].isdigit()):
        raise birthday_NotDate_exception
    if ((int(lst_cut[2]) < 0) or (1 > int(lst_cut[1]) or int(lst_cut[1])> 12) or (0 > int(lst_cut[0]) or int(lst_cut[0]) > 31)) or (int(lst_cut[1]) == 2 and int(lst_cut[0]) > 29):
        raise birthday_WrongDate_exception
    return None 

def database_execute(db_parse : str, get_info:list = None):
    try:
        db = sqlite3.connect("database.db")
        curs = db.cursor()
        curs.execute(db_parse)
        db.commit()
        if get_info != None:
            get_info += list(curs)[:]
        db.close()
    except Exception:
        logging.critical("DataBase: " + db_parse)
        raise database_exeption

#---------[bot_exceptions]-----------
class birthday_NotDate_exception(Exception): pass
class birthday_WrongFormat_exception(Exception): pass
class birthday_WrongDate_exception(Exception): pass
class database_exeption(Exception):pass
