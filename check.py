for my in myhobby:
    for notmyhobby in res:
        if my in notmyhobby[1]:
            res1 = db.get_user(notmyhobby[0])
            if str(res1[0][0]) == None:
                bot.send_message(message.chat.id, 'No Image')
            else:
                bot.send_message(message.chat.id, res1[0][1])
            bot.send_message(message.chat.id, res1[0][1])
            bot.send_message(message.chat.id, res1[0][2])
            bot.send_message(message.chat.id, res1[0][3])
            bot.send_message(message.chat.id, '@' + str(res1[0][4]))
            res.remove(notmyhobby)
        bot.register_next_step_handler(message, search, message, res)
        if len(res) == 0:
            bot.register_next_step_handler(message, start)

def search(message, myhobby, res):
    if message.text == 'следующий':
        my = myhobby[0]
        notmyhobby = res[0]
        if my in notmyhobby[1]:
            res1 = db.get_user(notmyhobby[0])
            if str(res1[0][0]) == None:
                bot.send_message(message.chat.id, 'No Image')
            else:
                bot.send_message(message.chat.id, (res1[0][0])
            bot.send_message(message.chat.id, res1[0][1])
            bot.send_message(message.chat.id, res1[0][2])
            bot.send_message(message.chat.id, res1[0][3])
            bot.send_message(message.chat.id, '@' + str(res1[0][4]))
        res.remove(notmyhobby)
        bot.register_next_step_handler(message, ssearch, message, res)
        if len(res) == 0:
            bot.register_next_step_handler(message, start)
