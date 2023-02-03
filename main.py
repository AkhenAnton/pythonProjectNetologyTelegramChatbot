# First try to create Telegram Chatbot

import random

import telebot

token = '6065768709:AAFULr1a3pmNtGJhC6TxYmRP_gJ5YSL3cWc'

bot = telebot.TeleBot(token)

HELP = """
/help - вывести список доступных команд.
/show - напечатать все добавленные задачи.
/add - добавить задачу в список (название задачи запрашиваем у пользователя).
/random - добавить случайную задачу в список на дату 'Сегодня'.
/exit - выход из программы.
"""

todos = {}

RANDOM_TASKS = ['RANDOM_TASK_1', 'RANDOM_TASK_2', 'RANDOM_TASK_3', 'RANDOM_TASK_4']


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ''.join([tail])
    if len(task) <= 3:
        bot.send_message(message.chat.id, 'Error. Task is very short. Length of task must be more than 3 symbols.')
    else:
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Task {task} added to date {date}')


@bot.message_handler(commands=['random'])
def random_add(message):
    task = random.choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    print(message.text)
    bot.send_message(message.chat.id, f'Task {task} added to date сегодня')


@bot.message_handler(commands=['show'])
def show(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)


# Constant access to the Telegram servers
bot.polling(none_stop=True)
