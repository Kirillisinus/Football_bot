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
rank = "TRAINEE I"

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

    #user = User(message.from_user.first_name, 0)

    if (text != "/reg" and text != "/reg@qakickerratingbot") and not results:
        bot.send_message(chat_id, "Ты даже не зарегался\nНапиши /reg, рак")
    elif text == "/help" or text == "/help@qakickerratingbot":   
        bot.send_message(message.chat.id, '/reg - регистрация на игру\n /win - добавление очков после победы\n /lose - снятие очков после поражения\n /allstats - общая статистика\n /mystat - твоя статистика')
    elif text == "/reg" or text == "/reg@qakickerratingbot":
        if not results:
            cursor = conn.cursor()
            sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
            #data = (user.getName(), user.getScope())
            data = (message.from_user.first_name, 0)

            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            
            bot.send_message(chat_id, message.from_user.first_name + ', ты зарегался и сейчас у тебя 0 очков. Твой ранг - %s.' % rank)
        else:
            bot.send_message(chat_id, message.from_user.first_name + ', ты уже зарегался')
    elif text == "/win" or text == "/win@qakickerratingbot":
        cursor = conn.cursor()
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (message.from_user.first_name,)
        cursor.execute(sqlSEL, data)
        user_scope = cursor.fetchall()
        coins = user_scope[0][0]
        coins+=25

        sqlUPD = "UPDATE users SET scope = %s WHERE tg_name = %s;"
        data = (coins, message.from_user.first_name)
        cursor.execute(sqlUPD, data)
        
        conn.commit()
        cursor.close()

        bot.send_message(chat_id, 'Хорош, добавляю тебе 25 очков')
    elif text == "/lose" or text == "/lose@qakickerratingbot":
        cursor = conn.cursor()
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (message.from_user.first_name,)
        cursor.execute(sqlSEL, data)
        user_scope = cursor.fetchall()
        coins = user_scope[0][0]
        
        if(coins==0):
            bot.send_message(message.chat.id, 'Не от чего отмнимать рейтинг')
            return
        elif(coins < 25 and coins >= 0):
            coins = 0
        else:
            coins -=25
        
        sqlUPD = "UPDATE users SET scope = %s WHERE tg_name = %s;"
        data = (coins, message.from_user.first_name)
        cursor.execute(sqlUPD, data)
        conn.commit()
        cursor.close()

        bot.send_message(chat_id, 'Как так можно было? Отнимаю 25 очков')
    elif text == "/mystat" or text == "/mystat@qakickerratingbot": 
        cursor = conn.cursor()
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (message.from_user.first_name,)
        cursor.execute(sqlSEL, data)
        my_scope = cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        cursor.execute(sql)
        grades = cursor.fetchall()
        cursor.close()

        j = 0
        for i in grades:
            if i[1] > my_scope[0][0]:
                if(j == 0):
                    j += 1
                
                rank = i[0]
                break
            else:
                j += 1
                

        bot.send_message(chat_id, message.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % rank)
            
    elif text == "/allstats" or text == "/allstats@qakickerratingbot":
        cursor = conn.cursor()
        sqlSEL = "SELECT tg_name, scope FROM users"
        cursor.execute(sqlSEL)
        scopes_with_names = cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        cursor.execute(sql)
        grades = cursor.fetchall()
        cursor.close()

        j = 0
        for n in scopes_with_names:
            for i in grades:        
                if i[1] > n[1]:
                    bot.send_message(chat_id, n[0] + ', ранг - %s. Чего такой маленький?' % i[0])
                    break
                else:
                    j += 1

# Запускаем бота
bot.polling(none_stop=True, interval=0)
# cursor.close()
# conn.close()