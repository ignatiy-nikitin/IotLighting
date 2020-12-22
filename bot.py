from enum import Enum

import telebot
from telebot import types

from cloud import get_current_lighting, send_reference_lighting, send_reference_warmth
from cloud import get_reference_lighting
from cloud import get_current_warmth
from cloud import get_reference_warmth

TELEGRAM_BOT_TOKEN = '1416755413:AAGkeWpfKNsl4jh9r0o0_n3aOpJ-f7X8Qig'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

GET_LIGHTING_INFO = 'получить информацию об освещении'
SET_REFERENCE_LIGHTING = 'выставить рекомендуемое освещение'
SET_REFERENCE_WARMTH = 'выставить рекомендуемое значение теплоты освещения'

markup = types.ReplyKeyboardMarkup()
markup.row(GET_LIGHTING_INFO)
markup.row(SET_REFERENCE_LIGHTING)
markup.row(SET_REFERENCE_WARMTH)

back_markup = types.ReplyKeyboardMarkup()
back_markup.row('назад')


class Modes(Enum):
    START = 1
    SET_REFERENCE_LIGHTING = 2
    SET_REFERENCE_WARMTH = 3


current_mode = Modes.START


@bot.message_handler(commands=['start'])
def welcome(message):
    global current_mode
    text = 'Система управления освещением.\n' \
           'Отправте команду и мы ее выполним.'
    bot.send_message(message.chat.id, text, reply_markup=markup)
    current_mode = Modes.START


@bot.message_handler(content_types=['text'])
def comands(message):
    global current_mode, markup, back_markup
    if current_mode == Modes.START:
        if message.text == GET_LIGHTING_INFO:
            text = 'Текущее значение освещения: {} lux\n' \
                   'Выставленное рекомендованное значение освещения: {} lux\n' \
                   'Текущее значение теплоты освещения: {}%\n' \
                   'Выставленное рекомендованное значение теплоты освещения: {}%\n'.format(get_current_lighting(),
                                                                                           get_reference_lighting(),
                                                                                           get_current_warmth(),
                                                                                           get_reference_warmth())
            bot.send_message(message.chat.id, text, reply_markup=markup)
        elif message.text == SET_REFERENCE_LIGHTING:
            text = 'Отправьте значение рекомендованного освещения'
            bot.send_message(message.chat.id, text, reply_markup=back_markup)
            current_mode = Modes.SET_REFERENCE_LIGHTING
        elif message.text == SET_REFERENCE_WARMTH:
            text = 'Отправьте значение рекомендованной теплоты освещения'
            bot.send_message(message.chat.id, text, reply_markup=back_markup)
            current_mode = Modes.SET_REFERENCE_WARMTH
    elif current_mode == Modes.SET_REFERENCE_LIGHTING:
        if message.text == 'назад':
            current_mode = Modes.START
            text = 'Система управления освещением.\n' \
                   'Отправте команду и мы ее выполним.'
            bot.send_message(message.chat.id, text, reply_markup=markup)
            current_mode = Modes.START
        else:
            send_reference_lighting(int(message.text))
            text = 'Рекомендованное значение освещения успешно выставлено'
            bot.send_message(message.chat.id, text, reply_markup=markup)
            current_mode = Modes.START
    elif current_mode == Modes.SET_REFERENCE_WARMTH:
        if message.text == 'назад':
            current_mode = Modes.START
            text = 'Система управления освещением.\n' \
                   'Отправте команду и мы ее выполним.'
            bot.send_message(message.chat.id, text, reply_markup=markup)
            current_mode = Modes.START
        else:
            send_reference_warmth(int(message.text))
            text = 'Рекомендованная значение теплоты успешно выставлено'
            bot.send_message(message.chat.id, text, reply_markup=markup)
            current_mode = Modes.START


if __name__ == '__main__':
    bot.infinity_polling()
