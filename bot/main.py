import telebot
from telebot import types 
import requests
from dotenv import load_dotenv
import os
import json
from level import level_dict, level_answer, level_name, level_question
load_dotenv()
from gigachat import GigaChat


TG_TOKEN = os.getenv('TG_TOKEN')
GIGA_TOKEN = os.getenv('credentials')
bot = telebot.TeleBot(TG_TOKEN)

giga = GigaChat(
   credentials=GIGA_TOKEN,
   model="GigaChat-Pro",
)

headers = {
    'Content-Type': 'application/json'
}

base = types.InlineKeyboardButton(text='В главное меню', callback_data='base')
gigahelp = types.InlineKeyboardButton(text='Помощь гигачата', callback_data='gigahelp')


inline1 = types.InlineKeyboardMarkup()
teach = types.InlineKeyboardButton(text='Обучение', callback_data='teach')
tips = types.InlineKeyboardButton(text='Советы', callback_data='tips')
inline1.add(teach, base, tips)

inline2 = types.InlineKeyboardMarkup()
from_scratch = types.InlineKeyboardButton(text='Обнулить мой прогресс уроков', callback_data='from_scratch')
my_levels = types.InlineKeyboardButton(text='Все уроки', callback_data='my_levels')
current_level = types.InlineKeyboardButton(text='Текущий урок', callback_data='current_level')
inline2.add(from_scratch, my_levels, current_level, base)

inline3 = types.InlineKeyboardMarkup()
next_level = types.InlineKeyboardButton(text='Хочу следующий урок', callback_data='next_level')
inline3.add(next_level)

#обработка Старта
@bot.message_handler(commands=['start'])
def start(message):
    response = requests.get(f'http://127.0.0.1:8000/api/v1/chat/{message.chat.id}/')
    if response.status_code == 404:
        data = {
            'chat':f'{message.chat.id}',
            'name':f'{message.from_user.username}',
            'level':'1'
            }
        bot.send_message(
            message.chat.id, 
            text=f'Не видел тебя раньше,{message.from_user.username}, создал тебе местную учетку))',
            reply_markup=inline1)
        res = requests.post('http://127.0.0.1:8000/api/v1/chat/', headers=headers, data=json.dumps(data))
        print(f'Создан аккаунт с {res.status_code}')
    if response.status_code == 200:
        bot.send_message(
            message.chat.id, 
            text=f'Привет еще раз, {message.from_user.username}!!!',
            reply_markup=inline1)

    
def change_level(chat, level):
    if level <= 3:
        data = {
            'chat':f'{chat}',
            'level':f'{level}'
            }
        response = requests.patch('http://127.0.0.1:8000/api/v1/chat/1/', headers=headers, data=json.dumps(data))
        bot.send_message(
                chat, 
                text=f'Теперь на уроке {level}!'
                )
    else:
       bot.send_message(
                chat, 
                text=f'Ты достиг последнего уровня!'
                ) 

def create_answer_keyboard(k):
    markup = types.InlineKeyboardMarkup()
    # print(data)
    x = level_answer[f'{k}'].split(';')
    for i in range(4):
        print(f'level_{k}_answer_{i}')
        markup.add(types.InlineKeyboardButton(
            text=f'{x[i]}',
            callback_data=f'level_{k}_answer_{i}'
        ))
    markup.add(types.InlineKeyboardButton(
        text='В главное меню',
        callback_data='base'
    ))
    return markup


def send_test(chat, k):
    bot.send_message(
            chat, 
            text=level_question[f'{k}'],
            reply_markup= create_answer_keyboard(k)

            )


def send_level(chat, k):
    response = requests.get(f'http://127.0.0.1:8000/api/v1/chat/{chat}')
    data_dict = response.json()
    if k == 0: #текущий прогресс
        bot.send_message(
                chat, 
                text=level_dict[f'{data_dict['level']}'],
                )
        send_test(chat, data_dict['level'])
    else: #по уровню урока
        bot.send_message(
                chat, 
                text=level_dict[f'{k}'],
                reply_markup= inline3
        )



#создает клавиатуру всех уроков
def create_lessons_keyboard(data):
    markup = types.InlineKeyboardMarkup()
    # print(data)
    for i in range(1, int(data['level'])+1):
        markup.add(types.InlineKeyboardButton(
            text=f'Урок {i}',
            callback_data=f'level_{i}'
        ))
    markup.add(types.InlineKeyboardButton(
        text='Назад',
        callback_data='base'
    ))
    return markup

@bot.message_handler(func=lambda message: message.text.startswith("Гигачат!"))
def handle_help_message(message):
    response = giga.chat(f"{message.text}")
    bot.send_message(
            chat_id=message.chat.id,
            text=f'{response.choices[0].message.content}',
        ) 

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    response = requests.get(f'http://127.0.0.1:8000/api/v1/chat/{callback.message.chat.id}/')
    data_dict = response.json()
    if callback.data == 'from_scratch':
        #обнуляем уровень
        change_level(callback.message.chat.id, 1)
        bot.send_message(
            chat_id=callback.message.chat.id,
            text='Обучение',
            reply_markup=inline2
        )  

    elif callback.data == 'my_levels':
        bot.send_message(
            chat_id=callback.message.chat.id,
            text='Список всех уровней!',
            reply_markup=create_lessons_keyboard(response.json())
        ) 

    elif callback.data == 'base':
        bot.send_message(
            chat_id=callback.message.chat.id,
            text='Главное меню.',
            reply_markup=inline1)

    elif callback.data == 'teach':
        bot.send_message(chat_id=callback.message.chat.id, text='Обучение', reply_markup=inline2)

    elif callback.data == 'tips':
        bot.send_message(chat_id=callback.message.chat.id, text='Если хочешь спросить совета, напиши сообщение, которое начинается с слова "Гигачат!')
        bot.send_message(chat_id=callback.message.chat.id, text='Главное меню', reply_markup=inline1)
    
    elif callback.data == 'current_level':
        send_level(callback.message.chat.id, 0)

    elif callback.data == 'level_1':
        send_level(callback.message.chat.id, 1)
    
    elif callback.data == 'level_2':
        send_level(callback.message.chat.id, 2)

    elif callback.data == 'level_3':
        send_level(callback.message.chat.id, 3)

    elif callback.data == 'next_level':
        lvl = int(data_dict['level']) + 1
        change_level(callback.message.chat.id, lvl)
        bot.send_message(chat_id=callback.message.chat.id, text='Обучение',
                         reply_markup=inline2)

    elif callback.data == 'current_level':
        send_level(callback.message.chat.id, 0)
    
    elif callback.data == 'level_1_answer_2':
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил правильно! Мегахорош!', reply_markup=inline3)

    elif callback.data in ['level_1_answer_0', 'level_1_answer_1', 'level_1_answer_3']:
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил неправильно! Правильный ответ: 3. Если хочешь помощи нейросети, напиши сообщение в чат, которое начинается с "Гигачат!', reply_markup=inline3)

    elif callback.data == 'level_2_answer_1':
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил правильно! Мегахорош!', reply_markup=inline3)

    elif callback.data in ['level_2_answer_0', 'level_2_answer_2', 'level_2_answer_3']:
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил неправильно! Правильный ответ: 2. Если хочешь помощи нейросети, напиши сообщение в чат, которое начинается с "Гигачат!', reply_markup=inline3)

    elif callback.data == 'level_3_answer_3':
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил правильно! Мегахорош!', reply_markup=inline3)

    elif callback.data in ['level_3_answer_0', 'level_3_answer_1', 'level_3_answer_2']:
        bot.send_message(chat_id=callback.message.chat.id, text='Ты ответил неправильно! Правильный ответ: 4. Если хочешь помощи нейросети, напиши сообщение в чат, которое начинается с "Гигачат!', reply_markup=inline3)


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка соединения: ', e)
except Exception as r:
    print("Непридвиденная ошибка: ", r)
finally: 
    print("Здесь всё закончилось")