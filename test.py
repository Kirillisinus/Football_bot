import psycopg2
from collections import defaultdict
import telebot
from telebot import types

TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
 
user = 'postgres'
password = '1234'
db_name = 'test'
host='localhost'
port = 5432
rank = "default"

conn = psycopg2.connect(dbname=db_name, user=user, 
                        password=password, host=host)

class User:
    def __init__(self, name, scope):
        self.__tg_name=name
        self.__scope=scope

    def setName(self) : return
    def setScope(self, newScope):
        self.__scope=newScope

    def getName(self):
        return self.__tg_name
    def getScope(self):
        return self.__scope

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Я - бот для подсчета вашего футбольного рейтинга \nЯ знаю всего несколько команд:\n /reg - регистрация на игру\n /win - добавление очков после победы\n /lose - снятие очков после поражения\n /allstats - общая статистика\n /mystat - твоя статистика')

@bot.message_handler(content_types=["text"])
def handle_text(message): 
    text = message.text.lower()
    chat_id =  message.chat.id

    cursor = conn.cursor()
    sql = """SELECT * FROM users WHERE tg_name = %s;"""
    data = (message.from_user.first_name,)
    cursor.execute(sql, data)
    results = cursor.fetchall()
    cursor.close()

    if (text != "/reg" and text != "/reg@qakickerratingbot") and not results:
        bot.send_message(chat_id, "Ты даже не зарегался\nНапиши /reg, рак")
    elif text == "/help" or text == "/help@qakickerratingbot":   
        bot.send_message(message.chat.id, '/reg - регистрация на игру\n /win - добавление очков после победы\n /lose - снятие очков после поражения\n /allstats - общая статистика\n /mystat - твоя статистика')
    elif text == "/reg" or text == "/reg@qakickerratingbot":
        if not results:
            user = User(message.from_user.first_name, 0)

            cursor = conn.cursor()
            sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
            data = (user.getName(), user.getScope())

            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            
            bot.send_message(chat_id, message.from_user.first_name + ', ты зарегался и сейчас у тебя 0 очков. Твой ранг - %s.' % rank)
        else:
            bot.send_message(chat_id, message.from_user.first_name + ', ты уже зарегался')
    elif text == "/win" or text == "/win@qakickerratingbot":
        if bool(user_REGby_messages[message.from_user.id]) == True:
            if bool(user_scores[message.from_user.id]) == False:
                user_scores[message.from_user.id] = 25
                bot.send_message(message.chat.id, 'Хорош, добавляю тебе 25 очков')
            else:               
                user_scores[message.from_user.id] =  int(user_scores[message.from_user.id]) + 25
                bot.send_message(message.chat.id, 'Хорош, добавляю тебе 25 очков')
        else:
            bot.send_message(message.chat.id, message.from_user.first_name + ', сначала зарегайся')
    elif text == "/mystat" or text == "/mystat@qakickerratingbot": 
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
    elif text == "/lose" or text == "/lose@qakickerratingbot":
        if bool(user_scores[message.from_user.id]) == True:
            user_scores[message.from_user.id] =  int(user_scores[message.from_user.id]) - 25
            bot.send_message(message.chat.id, 'Как так можно было? Отнимаю 25 очков')
        elif bool(user_scores[message.from_user.id]) == False:
            bot.send_message(message.chat.id, 'Не от чего отмнимать рейтинг')
    elif text == "/allstats" or text == "/allstats@qakickerratingbot":
        cursor = conn.cursor()
        sum = 0
        for row in cursor.execute("SELECT * FROM users"):   
            print(row + "\n" + type(row))
            #bot.send_message(message.chat.id, str(userNames[i]) + ' - ' + str(user_scores[i]) + ' очков')
        
        cursor.close()

# cursor = conn.cursor()
# cursor.execute("SELECT * FROM users")
# results = cursor.fetchall()
# print(results)
# cursor.close()

# Запускаем бота
bot.polling(none_stop=True, interval=0)
# cursor.close()
# conn.close()