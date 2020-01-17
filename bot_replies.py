start,add,delete,change,show,show_friends,add_request,delete_request,change_request,wrong_format,wrong_date,not_a_date, not_admin,empty_database,empty_request,empty_month = range(16)

bot_reply = {
    start          : "Greetings! I am BIRTHDAY-bot. I'll help you with your amnesia. Choose option to proceed",
    add            : "To add your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo add you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can add multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000",
    delete         : "To delete your own birthday, simply type: 'me'.\nTo delete your friend's birthday, enter his username: @BFF.\nYou can delete multiple birthdays too: @BFF,@BFF",
    change         : "To change your own birthday, simply enter it in format: 'DD.MM.YYYY'.\nTo change you buddy enter his username and birthday just like this: '@BFF = 26.03.2001'\nYou can change multiple friends too: @BFF,@BFF = 26.03.1999,11.11.1000",
    show           : "Choose an option",
    show_friends   : "To see your own birthday, simply type: 'me'.\nTo see your friend's birthday, enter his username: @BFF.\nYou can see multiple birthdays too: @BFF,@BFF",
    
    add_request    : "Thanks. I updated your birthday.",
    delete_request : "Thanks. I deleted all mentioned entries of your friends birthday !",
    change_request : "Thanks. I updated your birthday.",

    wrong_format   : "Wrong format!",
    wrong_date     : "Date is wrong!",
    not_a_date     : "Your date is no recognized as a date!",
    not_admin      : "Sorry, but only administrators can delete other users",
    empty_database : "No birthdays in your database",
    empty_request  : "No match found!",
    empty_month    : "No birthdays in this month"
}

