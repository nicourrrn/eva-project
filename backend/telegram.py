import os

import jwt
import telebot
import time
from pymongo import (
    MongoClient,
    collection
)

bot = telebot.TeleBot(os.getenv("TOKEN"))
admin_id = os.getenv("ADMIN_ID")

client = MongoClient("localhost", 27017)
users: collection.Collection = client.eva_project.users


@bot.message_handler(["start"])
def start(message: telebot.types.Message):
    users_name = list(map(lambda u: u["username"], users.find()))
    username = message.from_user.username
    if username not in users_name:
        bot.send_message(admin_id, f"@{message.from_user.username} would like start me")
        return
    token = jwt.encode(
        {"username": message.from_user.username},
        key=os.getenv("ACCESS_KEY")
    )
    bot.send_message(message.chat.id, "Your token:")
    bot.send_message(message.chat.id, token)


@bot.message_handler(content_types=["text"])
def upload_status(message: telebot.types.Message):
    users_name = list(map(lambda u: u["username"], users.find()))
    username = message.from_user.username
    if username not in users_name:
        bot.send_message(admin_id, f"@{message.from_user.username} would like write text me")
        return
    words = message.text.split(" ")
    scope: int
    try:
        if 11 < (scope := int(words[0])) or scope < 0:
            bot.reply_to(message, "scope not from 1 to 10")
            return
    except Exception as e:
        bot.reply_to(message, str(e))
        return

    users.update_one({"username": message.from_user.username},
                     {"$push": {"statuses":
                                    {"scope": scope, "status": " ".join(words[1:]),
                                     "time": int(time.time())}
                                }})
    bot.send_message(message.chat.id, "Successful!")


bot.polling()
