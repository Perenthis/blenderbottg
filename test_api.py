from gigachat import GigaChat

giga = GigaChat(
   credentials="MDE5YmIzNWYtOGM2Ny03ZTlkLTk3YjAtMDc2ZWFhOGE3OTVjOmFiN2MyZmJlLWIwMzItNGU0Ny05YTM3LTc5OGFkNzQ2ZmNlYg==",
   model="GigaChat-Pro"
)
answer_true = 'Пространство, в котором создаются и располагаются объекты'
answer = 'Фильтры и эффекты для обработки изображений'
question = 'Что такое сцена в программе Blender?'
tema = 'Основы работы в Blender: знакомство со сценой и системой координат'
promt = f'Ты мой личный наставник по изучению программы Blender. Я изучаю тему{tema}. Мне задали вопрос {question}. Я ответил неправильно: {answer}. Правильный ответ: {answer_true}.'
response = giga.chat("Привет! Как дела?")

print(response.choices[0].message.content)