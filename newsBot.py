'''
Бот
-Регистрация пользователя по идентификатору VK (telegram).
Работа с подписками:
-Просмотреть/добавить/удалить подписки на категории новостей.
-Просмотреть/добавить/удалить подписки на ключевые слова.
-Получение списка из 10 наиболее релевантных новостей по активным подпискам.

-Таблица users для хранения зарегистрированных пользователей.
-Таблица categories для хранения списка подписок на категории для каждого пользователя.
-Таблица keywords для хранения списка подписок на ключевые слова для каждого пользователя.


 bot = telebot.TeleBot("1629080631:AAGJUScNV0kLMcLoges2Frj1xJRhSG6pHzk", parse_mode=None)

 @bot.message_handler(commands=['start', 'help'])
 def handle_start_help(message):
     bot.reply_to(message, "Я пока ничего не умею?")

 @bot.message_handler(func=lambda message: True)
 def answer_to_message(message):
     print(message.from_user.id)
     if message.text in list_hello:
         bot.send_message(message.from_user.id, "И тебе привет!")
 bot.polling()
'''
import sqlite3, telebot,requests
from newsapi import NewsApiClient

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, "Здравствуйте, представьтесь:")
    bot.register_next_step_handler(msg, regNewUser)
    
def initDB():
    """Подключение к БД и создание таблиц"""
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlCreateTableUsers = '''CREATE TABLE IF NOT EXISTS "users" (
                                    "id"	INTEGER NOT NULL,
                                    "name"	TEXT NOT NULL,
                                    PRIMARY KEY("id" AUTOINCREMENT));'''

        sqlCreateTableCategories = '''CREATE TABLE IF NOT EXISTS "categories" (
                                    "id"	INTEGER NOT NULL,
                                    "name"	TEXT NOT NULL,
                                    "user_id"	INTEGER NOT NULL,
                                    PRIMARY KEY("id" AUTOINCREMENT)
                                );'''
        sqlCreateTableKeywords = '''CREATE TABLE IF NOT EXISTS "keywords" (
                                    "id"	INTEGER NOT NULL,
                                    "name"	TEXT NOT NULL,
                                    "user_id"	INTEGER NOT NULL,
                                    PRIMARY KEY("id" AUTOINCREMENT)
                                );'''

        cursor = sqlConn.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlCreateTableUsers)
        sqlConn.commit()
        print("Таблица users создана")

        cursor.execute(sqlCreateTableCategories)
        sqlConn.commit()
        print("Таблица categories создана")

        cursor.execute(sqlCreateTableKeywords)
        sqlConn.commit()
        print("Таблица keywords создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к БД>", error)
    finally:
        if (sqlConn):
            sqlConn.close()
            print("Соединение с SQLite закрыто")

def addKeyword(message):
    userId = message.from_user.id
    keywords = message.text
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlite_insert_with_param = """INSERT INTO keywords
                                          (keywords, userId)
                                          VALUES (?, ?);"""
        data_tuple = (keywords, userId)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlConn.commit()
        print("Запись успешно вставлена в таблицу keywords ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()
            print("Соединение с SQLite закрыто")



def regNewUser(message):
    """ registration new user"""
    userId = message.from_user.id
    name = message.text
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlInsertNewUser = """INSERT INTO users
                                      (id, name)
                                      VALUES (?, ?);"""
        params = (userId, name)
        cursor.execute(sqlInsertNewUser, params)
        sqlConn.commit()
        print("Запись успешно вставлена в таблицу users ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()
            print("Соединение с SQLite закрыто")



#def getNews(userID,categories="дтп",domains="yandex.ru"):
def getNews(keyWord="Рос", domains="yandex.ru"):
    #get all sources of news support country/category
    #https://newsapi.org/v2/sources?apiKey=<api_key>&q=Россия&country=ru&language=ru
    #https://newsapi.org/v2/sources?apiKey=7e40013ca7ea498589545453e4cea074&q=Россия&country=ru&language=ru
    #everything
    #https://newsapi.org/v2/everything?apiKey=<api_key>&q=Россия&country=ru&language=ru


    #status string
    #If the request was successful or not. Options: ok, error. In the case of error a code and message property will be populated.

    # Init
    newsapi = NewsApiClient(api_key='7e40013ca7ea498589545453e4cea074')
    #get sources
    sources = newsapi.get_sources()
    print("src:",sources)

    top_headlines = newsapi.get_top_headlines( #q='bitcoin',
                                              sources='abc-news',
                                              #category='business',
                                              language='en')
                                              #country='us')Ы

    newsList = []

    #apiKey = "7e40013ca7ea498589545453e4cea074"
    #categories = "Россия"
    #domains = "yandex.ru"
    #requestNews = f"https://newsapi.org/v2/everything?q={categories}&domains={domains}&sortBy=publishedAt&apiKey={apiKey}"
    #print(requestNews)
    #response = requests.get(requestNews)
    #response = response.json()

    '''
    #only top10
    if len(response["articles"]) < 10:
        newsCount = len(response["articles"])
    else:
        newsCount = 10

    for i in range(newsCount):
        newsList.append({
            "title": response["articles"][i]["title"],
            "description": response["articles"][i]["description"],
            "url": response["articles"][i]["url"],
            "urlToImage": response["articles"][i]["urlToImage"],
            "publishedAt": response["articles"][i]["publishedAt"],
            "content": response["articles"][i]["content"],
        })
    '''
    #return newsList
    print (top_headlines)


categoryList=['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
language = 'ru'
country = 'ru'

initDB()
#authorization

#bot = telebot.TeleBot("1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM", parse_mode=None)

getNews()
#regNewUser()

#start bot
#bot.polling()