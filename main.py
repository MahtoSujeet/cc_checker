from pyrogram import Client, filters
from api import lerachapter_20
from tg_helper import TgBot
from pyrogram.types import Message
import time
import os

# bot details
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")


# chk card checking function
def chk(data, update, message: Message):
    tgbot = TgBot(update, message)
    tgbot.card = data
    start = time.time()
    checker = lerachapter_20.Checker(data)
    res1 = checker.make_request_1()

    # If get checked in 1st request per se
    if not checker.request_1_done:
        tgbot.update_status_100(res1, str(time.time()-start)[:4])
        return

    # 2nd reqeust
    tgbot.update_status_50()
    res2 = checker.make_request_2()
    tgbot.update_status_100(res2, str(time.time()-start)[:4])
    if os.path.exists("res.html"):
        tgbot.send_document("res.html")


# Telegram bot initiation
tgbot = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Checking cmd
@tgbot.on_message(filters.command("chk"))
def chk_func(update, message: Message):
    arg = message.text
    try:
        data = arg.split(" ", maxsplit= 1)[1]
    except Exception:
        TgBot.reply_message("Please provide some argument! BSDK", update, message) 
        return
    chk(data, update, message)
    
@tgbot.on_message(filters.command("mchk"))
def mchk_func(update, message: Message):
    try:
        arg = message.text.split(" ", maxsplit= 1)[1]
        data = [card.strip() for card in arg.split("\n")]
    except Exception:
        TgBot.reply_message("No arguments passed! BSDK", update, message)
        return
    for card in data:
        chk(card, update, message)





print("Bot started!")
tgbot.run()

