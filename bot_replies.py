start,add,delete,change,show,show_friends,add_request,delete_request,change_request,wrong_format,wrong_date,not_a_date, not_admin,empty_database,empty_request,empty_month,sql_already_in,cancel,main_menu,show_menu,settings_menu,feedback,feedback_req,custom_wishes,wrong_input,custom_wishes_req,add_wish_request,add_wish,missed_sym,delete_wishes,empty_list,wishes_menu,no_username = range(33)

bot_reply = {
    start                   : "_Greetings human 👋!\nI am 🎉🤡🍾-bot. I'll help you with your (◐▂◑ ).\nI work only with usernames,so you should have one!\nChoose option to 👌 _",
    add                     : "_To add your own birthday, simply enter it in format: _ *'DD.MM.YYYY'* _.\nTo add you buddy enter his username and birthday just like this: _ *@BFF = 26.03.2001'* _ \nYou can add multiple friends too: _ *@BFF,@BFF = 26.03.1999,11.11.1000*",
    delete                  : "_To delete your own birthday, simply type: _ *'me'* _.\nTo delete your friend's birthday, enter his username: _ *@BFF* _.\nYou can delete multiple birthdays too: _ *@BFF,@BFF*",
    change                  : "_To change your own birthday, simply enter it in format: _ *'DD.MM.YYYY'* _.\nTo change you buddy enter his username and birthday just like this: _ *@BFF = 26.03.2001'* _ \nYou can change multiple friends too: _ *@BFF,@BFF = 26.03.1999,11.11.1000*",
    show                    : "_Choose an option _",
    show_friends            : "_To see your own birthday, simply type: _ *'me'* _.\nTo see your friend's birthday, enter his username: _ *@BFF* _.\nYou can see multiple birthdays too: _ *@BFF,@BFF*",
    feedback                : "_Send me feedback , and I`ll read it...maybe _",
    add_wish                : """_To add your wish, simply send me a text with {0} in it. It's necessarily for showing names of your friends!\nYou can also send me multiple wishes using splitor ###: *your text* ### *your text* _""",
    delete_wishes           : "*Thanks. I've deleted all custom wishes*",

    add_request             : "*Thanks. I've added requested birthdays.*",
    delete_request          : "*Thanks. I've deleted all mentioned birthdays!*",
    change_request          : "*Thanks. I've changed requested birthdays.*",
    feedback_req            : "*Thanks, I've sent your feedback*",
    custom_wishes_req       : "*Thanks, I've updated your settings*" ,
    add_wish_request        : "*Thanks. I've added all your wishes.*",
 
    cancel                  : "*Returning to main menu*",
    wrong_format            : "*Wrong format!*",
    wrong_date              : "*Date is wrong!*",
    not_a_date              : "*Your date is no recognized as a date!*",
    not_admin               : "*Sorry, but only* _ administrators _ *can delete/change other users*",
    empty_database          : "*No birthdays in your database*",
    empty_request           : "*No match found!*",
    empty_month             : "*No birthdays in this month*",
    sql_already_in          : "* Note: those users were not added (already in database):* ",
    wrong_input             : "*Can't recognize input*",
    missed_sym              : "* {0} is missed!*",
    empty_list              : "*There is no custom wishes in your group!*",
    no_username             : "*😥, but I work only with usernames...and you don't have one.\nCome back, with your brand-new username and I'll open my 💖 for you!*"
}

bot_birthday_msg =[
                    "_ Count your life by smiles, not tears. Count your age by friends, not years. _ 🎂 * Happy birthday, * {0}! 🎂",
                    " 🎉* Happy birthday, *  {0} 🎉\n _ ! I hope all your birthday wishes and dreams come true. _",
                    "_ A wish for _ {0} _ on your birthday, whatever you ask may you receive, whatever you seek may you find, whatever you wish may it be fulfilled on your birthday and always. _ 🎁 * Happy birthday * 🎁 ",
                    "_ Another adventure filled year awaits you. Welcome it by celebrating _ {0} _ birthday with pomp 🎉 and splendor. _ * Wishing you a very happy and fun-filled 🤡 birthday * ",
                    "_ May the joy_ 🤡 _ that _ {0} _ have spread in the past come back to you on this day. _ * Wishing you a very happy birthday * 🎂 ",
                    " 🎉 * Happy birthday! * 🎉 _ {0} _ life is just about to pick up speed and blast off into the stratosphere. Wear a seat belt and be sure to enjoy the journey. _ ",
                    "_ This birthday, I wish _ {0} _ abundant _ 😁 _ and _ ❤️ _. May all your dreams turn into reality and may lady luck visit your home today. _ 🎉 * Happy birthday to one of the sweetest people I’ve ever known. * 🎉",
                    "_ May you be gifted with life’s biggest joys and never-ending bliss. After all, you yourself are _ 💎 _ to earth, so you deserve the best. _  🎂 * Happy birthday, * {0} 🎂",
                    "_ Count not the candles…see the lights they give. Count not the years, but the life you live. Wishing _ {0} _ a wonderful _ ⌛️ _ ahead. _ 🎉 * Happy birthday.  * 🎉",
                    "_ Forget the past; look forward to the _ 🕕 _, for the best things are yet to come. _ {0} ",
                    "_ Birthdays are a new start, a fresh beginning and a _ 🕕 _ to pursue new endeavors with new goals. Move forward with confidence and courage. _ 💎 {0} 💎 _ are a very special person. May today and all of your days be amazing! _ ",
                    " {0} _ birthday is the first day of another 365-day journey. Be the shining thread in the beautiful tapestry of the world to make this year the best ever. Enjoy the _ 💰 _ . _ ",
                    " 🍾 * Be happy! * 🍾 _ Today is the day _ {0} _ were brought into this world to be a blessing and inspiration to the people around you! You are a _ 💎 _ person! May you be given more birthdays to fulfill all of your dreams!  _",
]

bot_keyboard = {
    main_menu     : [['🎉ADD🎉','🔎SHOW🔎'],['✏️CHANGE✏️','🧹DELETE🧹'],['✍️WISHES✍️','⚙️SETTINGS⚙️']],
    show_menu     : [['📆CURRENT📆','🥳FRIENDS🥳','🌎ALL🌎'],['◀️BACK◀️']],
    settings_menu : [['☄️USE_CUSTOM_WISHES☄️'],['📧FEEDBACK📧'],['◀️BACK◀️']],
    custom_wishes : [['❌OFF❌','✅ON✅']],
    wishes_menu   : [['➕ADD➕','🗑️DELETE_ALL🗑️','📋SHOW📋'],['◀️BACK◀️']]

}
