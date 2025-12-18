import telebot
from telebot import types 

token = '8201498258:AAEQF_ubDnxpxWo0RaKj8UCzUnziQO6Du80'
bot = telebot.TeleBot(token) 

lessons = {
    1: {
        'name': 'Основы основ',
        'sublessons': {
            1: {
                'name': 'Основы интерфейса',
                'content': 'Сюда содержимое подурока 1.1',
                'test': 'Сюда тестик для 1.1',
                'test_ans': 'Сюда ответик для 1.1'
            },
            2: {
                'name': 'Навигация',
                'content': 'Содержание подурока 1.2',
                'test': 'Тест для 1.2',
                'test_ans': 'Ответ 1.2'
            }
        }
    }
}
created_sublessons = {1: [1]}

#обработка Старта
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет! Я интеллектуальный бот-помощник для новичков в программе блендере. Если хочешь начать обучение напиши "Поехали!"')

inline1 = types.InlineKeyboardMarkup()
ik = types.InlineKeyboardButton(text='Начать обучение', callback_data='start_learn')
ik2 = types.InlineKeyboardButton(text='Все заново', callback_data='again')
inline1.add(ik, ik2)

inline2 = types.InlineKeyboardMarkup()
ik3 = types.InlineKeyboardButton(text='С нуля', callback_data='from_scratch')
ik4 = types.InlineKeyboardButton(text='Хоткеи', callback_data='hotkeys')
ik5 = types.InlineKeyboardButton(text='Советы', callback_data='tips')
inline2.add(ik3, ik4, ik5)

def create_lessonbtn(lesson_num, sublesson_num):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text=f'Пройти тест {lesson_num}.{sublesson_num}',
        callback_data='no_action'  # Просто заглушка, чтобы кнопка работала ( ЭТУ ТОЖЕ)
    ))
    markup.add(types.InlineKeyboardButton(
        text='Назад к уроку',
        callback_data='no_action'  # Просто заглушка ( ЭТУ ШТУКУ НЕ Я ПИСАЛ)
    ))
    return markup
# ЭТО ДЛЯ СОЗДЯНИЯ КНОПОЧЕК 
def create_btn(lesson_num, sublesson_num):
    markup = types.InlineKeyboardMarkup()
    next_sub = sublesson_num + 1 
    if next_sub in lessons[lesson_num]['sublessons']:
        if next_sub in created_sublessons[lesson_num]:
            markup.add(types.InlineKeyboardButton(
                text=f'Подурок {lesson_num}.{next_sub}',
                callback_data='no_action'
            ))
    else:
        next_lesson = lesson_num + 1
        if next_lesson not in created_sublessons:
            created_sublessons[next_lesson] = []
            created_sublessons[next_lesson].append(1)
            markup.add(types.InlineKeyboardButton(
                text=f'Урок {next_lesson}',
                callback_data='no_action'  # эту шнягу тоже
            ))
        
        markup.add(types.InlineKeyboardButton(
            text=f'Вернуться к подуроку {lesson_num}.{sublesson_num}',
            callback_data='no_action'
        ))
    
    markup.add(types.InlineKeyboardButton(
        text='Назад к урокам',
        callback_data='no_action'
    ))
    return markup
#                                           ЭТЯ ДЛЯ УРОКОВ
def create_lessons_keyboard():
    markup = types.InlineKeyboardMarkup()
    for lesson_num in created_sublessons.keys():
        markup.add(types.InlineKeyboardButton(
            text=f'Урок {lesson_num}',
            callback_data='no_action'
        ))
    markup.add(types.InlineKeyboardButton(
        text='Назад',
        callback_data='no_action'
    ))
    return markup

#                           ЭТЯ КНОПОЧКИ ДЛЯ ПОДУРОКОВ
def create_sublessons_keyboard(lesson_num):
    markup = types.InlineKeyboardMarkup()
    if lesson_num in created_sublessons:
        for sub_num in created_sublessons[lesson_num]:
            sub_name = lessons[lesson_num]['sublessons'][sub_num]['name']  # В ЭТОЙ СТРОКЕ НИЧЕ НЕ ПОНЯЛ
            markup.add(types.InlineKeyboardButton(
                text=f'{lesson_num}.{sub_num} {sub_name}',
                callback_data='no_action'            #ЭТО ТОЖЕ НЕ Я, НО ЭТ НАДО
            ))
    markup.add(types.InlineKeyboardButton(
        text='Назад к урокам',
        callback_data='no_action'
    ))
    return markup


@bot.message_handler(content_types=["text"])
def distribution(message):
    print(message.text)
    if message.text == 'Поехали!':
        bot.send_message(
            message.chat.id, 
            text='Отлично! Тебе требуется полное обучение с нуля, или может хоткеи? Или советы?',
            reply_markup=inline2)
    # ОБРАБОТКА КНОПКИ 1
    elif message.text == 'Урок 1':
        bot.send_message(
            message.chat.id,
            'Выбери подурок:',
            reply_markup=create_sublessons_keyboard(1)
        )
    
    # ОБРАБОТКА КНОПКИ 1.1
    elif message.text == '1.1 Основы интерфейса':
        sublesson = lessons[1]['sublessons'][1]
        content = f'{sublesson["name"]}\n\n{sublesson["content"]}'
        
        bot.send_message(
            message.chat.id,
            content,
            reply_markup=create_lessonbtn(1, 1)
        )

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'from_scratch':
        bot.send_message(
            chat_id=callback.message.chat.id,
            text='Отлично! Начинаем обучение с нуля!',
            reply_markup=create_lessons_keyboard()
        )
                  
    elif callback.data == 'hotkeys':
        bot.send_message(chat_id=callback.message.chat.id, text='Раздел хоткеев еще в разработке!')
    elif callback.data == 'tips':
        bot.send_message(chat_id=callback.message.chat.id, text='Раздел советов стилл ин прогресс :(')
    
    elif callback.data == 'no_action':
        pass

try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка соединения: ', e)
except Exception as r:
    print("Непридвиденная ошибка: ", r)
finally: 
    print("Здесь всё закончилось")