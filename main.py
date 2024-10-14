import telebot
import webbrowser
import sqlite3
from telebot import types


bot = telebot.TeleBot(token='8002715394:AAEsBeVVFLVKird9hFFKDHm5Wtr7aw0Oz2I')
name = None
@bot.message_handler(commands=['start'])
def start(message):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))'
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Hi, now we will register you, what is your name?')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'write the password')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = f'INSERT INTO users (name, pass) VALUES ("{name}", "{password}")'
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Users Liat', callback_data='users'))
    bot.send_message(message.chat.id, 'The user is registered', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM users'
    cursor.execute(query)
    users = cursor.fetchall()
    info = ''
    for user in users:
        info += f'Name: {user[1]} Password: {user[2]}\n'

    cursor.close()
    connection.close()

    bot.send_message(call.message.chat.id, info)

# @bot.message_handler(commands=['start'])
# def start_button(message):
#     ''' Creating buttons that open under the introductory line '''
#
#     markup = types.ReplyKeyboardMarkup()
#     btn1 = types.KeyboardButton('Open Site')
#     markup.row(btn1)
#     btn2 = types.KeyboardButton('Delete Photo')
#     btn3 = types.KeyboardButton('Edit Photo')
#     markup.row(btn2, btn3)
#     file = open('./photo.jpg', 'rb')
#     bot.send_photo(message.chat.id, photo=file, reply_markup=markup)
#     # bot.send_message(message.chat.id, f'Hello, {message.chat.first_name}!', reply_markup=markup)
#     bot.register_next_step_handler(message, on_click)
#
# def on_click(message):
#     if message.text == 'Open Site':
#         bot.send_message(message.chat.id, 'Website is open!')
#     elif message.text == 'Delete Photo':
#         bot.delete_message(message.chat.id, 'Deleted Photo')
#
#
# @bot.message_handler(content_types=['photo'])
# def send_photo(message):
#     ''' Create buttons for the photos that the user sends '''
#
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Open Site', url='https://google.com')
#     markup.row(btn1)
#     btn2 = types.InlineKeyboardButton('Delete Photo', callback_data='delete')
#     btn3 = types.InlineKeyboardButton('Edit Photo', callback_data='edit')
#     markup.row(btn2, btn3)
#     bot.reply_to(message, 'Oh, you look so cute :)', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     ''' Function for button control '''
#
#     if callback.data == 'delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     elif callback.data == 'edit':
#         bot.edit_message_text('Edit photo, please', callback.message.chat.id, callback.message.message_id)
#
# @bot.message_handler(commands=['site', 'website'])
# def site(message):
#     ''' Going to the website '''
#     webbrowser.open('https://github.com/lixdxn')
#
#
# @bot.message_handler(commands=['start', 'hello'])
# def main(message):
#     ''' Make command start/hello with user name '''
#     bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')
#
# @bot.message_handler(commands=['help'])
# def main(message):
#     ''' Make command help with text '''
#     bot.send_message(message.chat.id, '<em><b> Help</b> Information</em>', parse_mode='html')
#
# @bot.message_handler()
# def info(message):
#     if message.text.lower() == 'hello':
#         bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! How can I help you?')
#     elif message.text.lower() == 'id':
#         bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)