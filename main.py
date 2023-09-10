import telebot
from telebot import types
from telebot.asyncio_handler_backends import StatesGroup

import db

db = db.BotDB('people.db')

bot = telebot.TeleBot('6444670038:AAEYO5l-SpKnd1viS8dAzUBZbNUXR0eC1Zg')


@bot.message_handler(commands=['edit_photo'])
def change_photo(message):
    bot.send_message(message.chat.id, "пришли новое фото")
    bot.register_next_step_handler(message, ch_photo)



def ch_photo(message):

    raw = message.photo[0].file_id
    print(raw)
    name = raw + '.jpg'
    file_info = bot.get_file(raw)
    daownloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(daownloaded_file)
    img = open(name, 'rb')
    db.change_photo(None, message.from_user.id)


@bot.message_handler(commands=['search'])
def ssearch(message):
    res = db.select_all_hobby(message.from_user.id)
    myhobby = db.get_intrrest(message.from_user.id)
    myhobby = myhobby[0][0].split(';')

    for my in myhobby:
        for notmyhobby in res:
            if my in notmyhobby[1]:
                res1 = db.get_user(notmyhobby[0])
                if str(res1[0][0]) == 'None':
                    bot.send_message(message.chat.id, 'No Image')
                else:
                    bot.send_message(message.chat.id, str(res1[0][0]))
                bot.send_message(message.chat.id, res1[0][1])
                bot.send_message(message.chat.id, res1[0][2])
                bot.send_message(message.chat.id, res1[0][3])
                bot.send_message(message.chat.id, '@' + str(res1[0][4]))
                res.remove(notmyhobby)
            if len(res) == 0:
                bot.register_next_step_handler(message, start)


@bot.message_handler(commands=['edit_description'])
def edit_description(message):
    bot.send_message(message.chat.id,
                     'Введи новое описпние')
    bot.register_next_step_handler(message, update_description)


def update_description(message):
    db.update_description(message.text, message.from_user.id)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Тебе доступны такие команды, как /start, /edit_photo, /edit_description, '
                                      '/help, /search')


# message.from_user.id, None, name, description, None, course, None, interests
@bot.message_handler(commands=['start'])
def start(message):
    if not db.user_exists(message.from_user.id):
#shared photo
        bot.send_message(message.chat.id, "Я вижу, что ты тут в первый раз, введи своё имя:")
        bot.register_next_step_handler(message,get_description)
    else:
        keyboad_markup = types.ReplyKeyboardMarkup(row_width=2)
        button_help = types.KeyboardButton('/help')
        button_editphoto = types.KeyboardButton('/edit_photo')
        button_editdescription = types.KeyboardButton('/edit_description')
        button_search = types.KeyboardButton('/search')
        keyboad_markup.add(button_help, button_editphoto, button_editdescription, button_search)
        bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboad_markup)


def get_description(message):
    bot.send_message(message.chat.id, "Опиши себя")
    user_data = {
        "name":message.text,
        "description": None,
        "course": None,
        "interests": None,
        "photo": None
    }
    bot.register_next_step_handler(message, get_course, user_data)


def get_course(message, user_data):
    user_data["description"] = str(message.text).lower()
    bot.send_message(message.chat.id, "На каком курсе ты учишься?")
    bot.register_next_step_handler(message, get_interests, user_data)


def get_interests(message, user_data):
    user_data["course"] = message.text
    bot.send_message(message.chat.id, "Кинь аватарку")
    bot.register_next_step_handler(message, photo, user_data)


@bot.message_handler(content_types=['photo'])
def photo(message, user_data):
    raw = message.photo[0].file_id
    print(raw)
    name = raw + '.jpg'
    file_info = bot.get_file(raw)
    daownloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(daownloaded_file)
    img = open(name, 'rb')
    user_data["photo"] = img
    bot.send_message(message.chat.id, "Чем ты любишь заниматься?")
    bot.register_next_step_handler(message, make_user, user_data)


def make_user(message, user_data):
    interest = str(message.text).split(" ")
    interest = ''.join(interest)
    user_data["interests"] = interest
    name = user_data["name"]
    description = user_data["description"]
    course = user_data["course"]
    interests = user_data["interests"]
    photo = user_data["photo"]

    db.create_user(message.from_user.id, photo, name, description, message.from_user.username, course, None, interests)
    if db.user_exists(message.from_user.id):
        bot.send_message(message.chat.id, 'Успешно!')
    else:
        bot.send_message(message.chat.id, 'Ошибка')


@bot.message_handler()
def get_user_text(message):
    if (message.text) != None:
        return str(message.text)
    else:
        bot.send_message(message.chat.id, 'Ты ничего не ввёл :(')


bot.polling(none_stop=True)
# spisy