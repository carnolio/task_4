import telebot

 #list_hello = ("Привет", "Здравствуй", "Hello")

 bot = telebot.TeleBot("1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM", parse_mode=None)

 @bot.message_handler(commands=['start', 'help'])
 def handle_start_help(message):
     bot.reply_to(message, "Я пока ничего не умею?")

 @bot.message_handler(func=lambda message: True)
 def answer_to_message(message):
     print(message.from_user.id)
     if message.text in list_hello:
         bot.send_message(message.from_user.id, "И тебе привет!")
 bot.polling()

import vk_api
import random
'''
api_key = "359549902a44324efa3787962802e91c30ffc36dbb8a0c46fd1b139aead1a0d058d8edb8b0d3250e9b283"

vk = vk_api.VkApi(token=api_key)
vk._auth_token()
while True:
    messanges = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
    if messanges["count"] >= 1:
        print(messanges)
        id = messanges['items'][0]["last_message"]["from_id"]
        first_name = vk.method("users.get", {'user_ids': id})[0]['first_name']
        if messanges["items"][0]['last_message']['text'] == "Привет":
'''