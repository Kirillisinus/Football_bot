from collections import defaultdict
import telebot
from telebot import types
# Создаем экземпляр бота
TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
user_scores = defaultdict(list)
user_REGby_messages = defaultdict(list)
userNames = defaultdict(list)
userReg = []
userScores = []
userReg.append(0)
score = 1000 
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Я - бот для подсчета вашего футбольного рейтинга \nЯ знаю всего несколько команд:\n /reg - регистрация на игру\n /win - добавление очков после победы\n /lose - снятие очков после поражения\n /allstats - общая статистика\n /mystat - твоя статистика')
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебе ?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "/help" or message.text == "/help@QAKickerRatingBot":   
        bot.send_message(message.chat.id, '/reg - регистрация на игру\n /win - добавление очков после победы\n /lose - снятие очков после поражения\n /allstats - общая статистика\n /mystat - твоя статистика')
    elif message.text == "/reg" or message.text == "/reg@QAKickerRatingBot":
        if bool(user_REGby_messages[message.from_user.id]) == False:
            bot.send_message(message.chat.id, message.from_user.first_name + ', ты зарегался и сейчас у тебя 0 очков. Твой ранг - trainee footballer.')
            user_REGby_messages[message.from_user.id].append(1)
            userNames[message.from_user.id].append(message.from_user.first_name)
        else:
            bot.send_message(message.chat.id, message.from_user.first_name + ', ты уже зарегался')
    elif message.text == "/win" or message.text == "/win@QAKickerRatingBot":
        if bool(user_REGby_messages[message.from_user.id]) == True:
            if bool(user_scores[message.from_user.id]) == False:
                user_scores[message.from_user.id] = 25
                bot.send_message(message.chat.id, 'Хорош, добавляю тебе 25 очков')
            else:               
                user_scores[message.from_user.id] =  int(user_scores[message.from_user.id]) + 25
                bot.send_message(message.chat.id, 'Хорош, добавляю тебе 25 очков')
        else:
            bot.send_message(message.chat.id, message.from_user.first_name + ', сначала зарегайся')
    elif message.text == "/mystat" or message.text == "/mystat@QAKickerRatingBot": 
        if bool(user_scores[message.from_user.id]) == False:
            bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков. Твой ранг - trainee footballer.')
        elif user_scores[message.from_user.id] >= 0 and user_scores[message.from_user.id] < 250:
            bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков. Твой ранг - trainee footballer.') 
        elif user_scores[message.from_user.id] >= 250 and user_scores[message.from_user.id] < 500: 
            bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков. Твой ранг - junior footballer.')
        elif user_scores[message.from_user.id] >= 500 and user_scores[message.from_user.id] < 700: 
            bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков. Твой ранг - middle footballer.')
        elif user_scores[message.from_user.id] >= 700: 
            bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков. Твой ранг - senior footballer.')
        #bot.send_message(message.chat.id, message.from_user.first_name + ', у тебя ' + str(user_scores[message.from_user.id]) + ' очков')  
    elif message.text == "/lose" or message.text == "/lose@QAKickerRatingBot":
        if bool(user_scores[message.from_user.id]) == True:
            user_scores[message.from_user.id] =  int(user_scores[message.from_user.id]) - 25
            bot.send_message(message.chat.id, 'Как так можно было? Отнимаю 25 очков')
        elif bool(user_scores[message.from_user.id]) == False:
            bot.send_message(message.chat.id, 'Не от чего отмнимать рейтинг')
    elif message.text == "/allstats" or message.text == "/allstats@QAKickerRatingBot":
        for i in userNames:           
            bot.send_message(message.chat.id, str(userNames[i]) + ' - ' + str(user_scores[i]) + ' очков')
# Запускаем бота
bot.polling(none_stop=True, interval=0)