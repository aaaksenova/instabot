# -*- coding: utf-8 -*-
TOKEN = '994502658:AAFaXwcE8-76fh52ZX_PY7vGzDV6GzSaeQA'

import telebot
import sqlite3


db_dict = {u'пацанские цитаты':'boys', u'ванильные цитаты':'girls', u'музыка':'songs', u'литература':'literature'}

def get_quote(table):
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()
    cur.execute("""
    SELECT quote
     FROM {}
        ORDER BY RANDOM()
        LIMIT 1;
    """.format(table))
    quote = cur.fetchall()
    return quote[0][0]

bot = telebot.TeleBot(TOKEN)

def menu():
    mark_up = telebot.types.InlineKeyboardMarkup()
    categories = [u'пацанские цитаты', u'ванильные цитаты', u'музыка', u'литература']
    for category in categories:
        item = telebot.types.InlineKeyboardButton(text = category, callback_data = category)
        mark_up.add(item)
    return mark_up

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''Привет! Я ИнстаБот.
Пришли мне фотографию, и я подберу для нее подпись в инстаграм.''')

@bot.message_handler(content_types= ["photo"])
def send_menu(message):
    bot.send_message(message.chat.id, 'Выбери категорию подписи!', reply_markup=menu())

@bot.callback_query_handler(func=None)
def callback(message):
    quote = get_quote(db_dict[message.data])
    bot.send_message(message.from_user.id, text = quote)
    bot.send_message(message.from_user.id, text = 'Понравилось? Присылай новое фото!')

#bot.polling(none_stop=True)
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)