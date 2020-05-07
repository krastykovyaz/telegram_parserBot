# !/usr/bin/python
# coding=utf-8
import telebot
import bs4
import parser
import requests
from task import Task
import markups as m


TOKEN = "1049752328:AAHiihjkpzigLllXXr7fzACcf3uL9ydmYJg"
bot = telebot.TeleBot(TOKEN)
task = Task()

# @bot.message_handler(content_types=['text'])
# def text_handler(message):
#     text = message.text.lower()
#     chat_id = message.chat.id
#     if text == "привет":
#         bot.send_message(chat_id, 'Привет, я бот - парсер хабра.')
#     elif text == "как дела?":
#         bot.send_message(chat_id, 'Хорошо, а у тебя?')
#     else:
#         bot.send_message(chat_id, 'Простите, я вам не понял :(')
#
# @bot.message_handler(content_types=['photo'])
# def text_handler(message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, 'Красиво.'
# @bot.message_handler(commands=['start'])
# def welcome(message):
# 	bot.send_message(message.chat.id, 'Привет, я парсер')


# @bot.message_handler(commands=['go'])
# def start_handler(message):
# 	chat_id = message.chat.id
# 	msg = bot.send_message(chat_id, 'Откуда парсить?')
# 	bot.register_next_step_handler(msg, askSource) #askSource
	# task.isRunning = 1


# def askSource(message):
# 	chat_id = message.chat.id
# 	text = message.text.lower()
# 	if text in task.names[0]:
# 		task.mySource = 'top'
# 		msg = bot.send_message(chat_id, 'За какой временной промежуток?')
# 		bot.register_next_step_handler(msg, askAge)
# 	elif text in task.names[1]:
# 		task.mySource = 'all'
# 		msg = bot.send_message(chat_id, 'Какой минимальный порог рейтинга?')
# 		bot.register_next_step_handler(msg, askRating)
# 	else:
# 		 msg = bot.send_message(chat_id, 'Такого раздела нет. Введите раздел корректно.')
# 		 bot.register_next_step_handler(msg, askSource)
# 		 return

# def askAge(message):
# 	chat_id = message.chat.id
# 	text = message.text.lower()
# 	if text not in task.filters[0]:
# 		msg = bot.send_message(chat_id, 'Такого временного промежутка нет. Введите порог корректно.')
# 		bot.register_next_step_handler(msg, askAge) #askSource
# 		return
# 	task.myFilter = task.filters_code_names[0][task.filters[0].index(text)]
# 	msg = bot.send_message(chat_id, 'Сколько страниц парсить?')
# 	bot.register_next_step_handler(msg, askAmount)


# def askRating(message):
# 	chat_id = message.chat.id
# 	text = message.text.lower()
# 	filters = task.filters[1]
# 	if text not in filters:
# 		msg = bot.send_message(chat_id, 'Такого порога нет. Введите порог корректно.')
# 		bot.register_next_step_handler(msg, askRating)
# 		return
# 	task.myFilter = task.filters_code_names[1][filters.index(text)]
# 	msg = bot.send_message(chat_id, 'Сколько страниц парсить?')
# 	bot.register_next_step_handler(msg, askAmount)


# def askAmount(message):
# 	chat_id = message.chat.id
# 	text = message.text.lower()
# 	if not text.isdigit():
# 		msg = bot.send_message(chat_id, 'Количество страниц должно быть числом. Введите корректно.')
# 		bot.register_next_step_handler(msg, askAmount)
# 		return
# 	if int(text) < 1 or int(text) > 11:
# 		msg = bot.send_message(chat_id, 'Количество страниц должно быть >0 и <11. Введите корректно.')
# 		bot.register_next_step_handler(msg, askAmount)
# 		return
# 	task.isRunning = 0
# 	output = ''
# 	if task.mySource == 'top':
# 		output = parser.getTitlesFromTop(int(text), task.myFilter)
# 	else:
# 		output = parser.getTitlesFromAll(int(text), task.myFilter)
# 	msg = bot.send_message(chat_id, output)
# bot.polling(none_stop=True)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Откуда парсить?', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
        task.isRunning = True

def askSource(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text in task.names[0]:
        task.mySource = 'top'
        msg = bot.send_message(chat_id, 'За какой временной промежуток?', reply_markup=m.age_markup)
        bot.register_next_step_handler(msg, askAge)
    elif text in task.names[1]:
        task.mySource = 'all'
        msg = bot.send_message(chat_id, 'Какой минимальный порог рейтинга?', reply_markup=m.rating_markup)
        bot.register_next_step_handler(msg, askRating)
    else:
        msg = bot.send_message(chat_id, 'Такого раздела нет. Введите раздел корректно.')
        bot.register_next_step_handler(msg, askSource)
        return

def askAge(message):
    chat_id = message.chat.id
    text = message.text.lower()
    filters = task.filters[0]
    if text not in filters:
        msg = bot.send_message(chat_id, 'Такого временного промежутка нет. Введите порог корректно.')
        bot.register_next_step_handler(msg, askAge)
        return
    task.myFilter = task.filters_code_names[0][filters.index(text)]
    msg = bot.send_message(chat_id, 'Сколько страниц парсить?', reply_markup=m.amount_markup)
    bot.register_next_step_handler(msg, askAmount)

def askRating(message):
    chat_id = message.chat.id
    text = message.text.lower()
    filters = task.filters[1]
    if text not in filters:
        msg = bot.send_message(chat_id, 'Такого порога нет. Введите порог корректно.')
        bot.register_next_step_handler(msg, askRating)
        return
    task.myFilter = task.filters_code_names[1][filters.index(text)]
    msg = bot.send_message(chat_id, 'Сколько страниц парсить?', reply_markup=m.amount_markup)
    bot.register_next_step_handler(msg, askAmount)

def askAmount(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Количество страниц должно быть числом. Введите корректно.')
        bot.register_next_step_handler(msg, askAmount)
        return
    if int(text) < 1 or int(text) > 5:
        msg = bot.send_message(chat_id, 'Количество страниц должно быть >0 и <6. Введите корректно.')
        bot.register_next_step_handler(msg, askAmount)
        return
    task.isRunning = False
    print(task.mySource + " | " + task.myFilter + ' | ' + text) #
    output = ''
    if task.mySource == 'top':
        output = parser.getTitlesFromTop(int(text), task.myFilter)
    else:
        output = parser.getTitlesFromAll(int(text), task.myFilter)
    msg = bot.send_message(chat_id, output, reply_markup=m.start_markup)

bot.polling(none_stop=True)