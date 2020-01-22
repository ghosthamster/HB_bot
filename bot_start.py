# -*- coding: utf-8 -*-
from bot_func import *
from telegram.ext import MessageHandler, PrefixHandler, Dispatcher,JobQueue, Filters, CommandHandler
import re

def main():
    updater = Updater(token='YOUR TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    #bot_hadlers_creation
    bot_start_handler = ConversationHandler([CommandHandler('start',bot_start)],{},[])
    bot_add_handler = ConversationHandler([PrefixHandler('🎉','ADD🎉',bot_add)],{request_add:[MessageHandler(Filters.text,bot_request_add)]},[])
    bot_del_handler = ConversationHandler([PrefixHandler('🧹','DELETE🧹',bot_del)],{request_del:[MessageHandler(Filters.text,bot_request_del)]},[])
    bot_change_handler = ConversationHandler([PrefixHandler('✏️','CHANGE✏️',bot_change)],{request_change:[MessageHandler(Filters.text,bot_request_change)]},[])
    bot_show_handler = ConversationHandler([PrefixHandler('🔎','SHOW🔎',bot_show)], {request_show:[PrefixHandler('🌎','ALL🌎',bot_show_all),PrefixHandler('◀️','BACK◀️',bot_cancel),PrefixHandler('📆','CURRENT📆',bot_show_current_month),ConversationHandler([PrefixHandler('🥳','FRIENDS🥳',bot_show_friends)],{friends_show:[MessageHandler(Filters.text,bot_request_show_friends)]},[],map_to_parent= {ConversationHandler.END : ConversationHandler.END })]},[])
    bot_settings_handler = ConversationHandler([PrefixHandler('⚙️','SETTINGS⚙️',bot_settings)],{request_settings:[PrefixHandler('🗑️','DELETE_ALL_WISHES🗑️',bot_delete_wishes),PrefixHandler('◀️','BACK◀️',bot_cancel),ConversationHandler([PrefixHandler('➕','ADD_CUSTOM_WISHES➕',bot_add_wish)],{request_add_wish : [MessageHandler(Filters.text,bot_add_wish_request)]},[],map_to_parent={ConversationHandler.END : ConversationHandler.END}),ConversationHandler([PrefixHandler('☄️','USE_CUSTOM_WISHES☄️',bot_custom_wishes)], {custom_wishes_request : [MessageHandler(Filters.text,bot_custom_wishes_request)]},[],map_to_parent= {ConversationHandler.END : ConversationHandler.END }),ConversationHandler([PrefixHandler('📧','FEEDBACK📧',bot_feedback)],{feedback_request : [MessageHandler(Filters.text,bot_feedback_request)]},[],map_to_parent= {ConversationHandler.END : ConversationHandler.END })]},[])
    bot_left_chat_handler = MessageHandler(Filters.status_update.left_chat_member,bot_left_chat)

    #bot_hadlers_registration
    dispatcher.add_handler(bot_add_handler)
    dispatcher.add_handler(bot_start_handler)
    dispatcher.add_handler(bot_del_handler)
    dispatcher.add_handler(bot_change_handler)
    dispatcher.add_handler(bot_show_handler)
    dispatcher.add_handler(bot_settings_handler)
    dispatcher.add_handler(bot_left_chat_handler)
    
    #Job
    file = open("tasker.txt","r+")
    check = file.read()
    if not check == str(datetime.datetime.now().date()):
        Tasker = updater.job_queue
        Tasker.set_dispatcher(updater.dispatcher)
        Tasker.run_once(bot_reminder,2)
        file.close()
        
        file = open("tasker.txt","w")
        file.write(str(datetime.datetime.now().date()))

    file.close()

    #bot_start
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
