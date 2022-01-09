from pyrogram import Client, filters
from api import lerachapter_20
from tg_helper import TgBot
from pyrogram.types import Message
import time
import os


# Telegram bot initiation
tgbot = Client("bot")

# Checking cmd
@tgbot.on_message(filters.command("chk"))
def chk_func(update, message: Message):
    arg = message.text
    tgbot = TgBot(update, message)
    try:
        data = arg.split(" ", maxsplit= 1)[1]
    except IndexError:
        tgbot.edit_message("No arguments passed!")
        return
    start = time.time()
    checker = lerachapter_20.Checker(data)
    res1 = checker.make_request_1()

    # If get checked in 1st request per se
    if not checker.request_1_done:
        tgbot.update_status_100(res1, time.time()-start)
        return

    # 2nd reqeust
    tgbot.update_status_50()
    res2 = checker.make_request_2()
    tgbot.update_status_100(res2, time.time()-start)
    if os.path.exists("res.html"):
        tgbot.send_document("res.html")




print("Bot started!")
tgbot.run()
