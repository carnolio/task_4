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


'''

import sqlite3
import telebot
import requests
#from telebot import types

def connectToDB():
    """Подключение к БД и создание таблиц"""
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlCreateTableUsers = '''CREATE TABLE IF NOT EXISTS "users" (
                                    "id"	INTEGER NOT NULL,
                                    "telegram_id"	INTEGER NOT NULL,
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

#def getNews(userID,categories="дтп",domains="yandex.ru"):
def getNews(categories="Рос", domains="yandex.ru"):
    newsList = []
    apiKey = "7e40013ca7ea498589545453e4cea074"
    #categories = "Россия"
    #domains = "yandex.ru"
    requestNews = f"https://newsapi.org/v2/everything?q={categories}&domains={domains}&sortBy=publishedAt&apiKey={apiKey}"
    print(requestNews)
    response = requests.get(requestNews)
    response = response.json()

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
    return newsList


connectToDB()
print(getNews())