from pyrogram import Client, filters
from api import lerachapter_20, feedingamerica
from tg_helper import TgBot
from pyrogram.types import Message
import os


# bot details
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")


# chk card checking function
def chk(data, update, message: Message):
    tgbot = TgBot(update, message)
    tgbot.card = data # THis is waht bot sends in  result msg
    checker = lerachapter_20.Checker(data)
    try:
        res1 = checker.make_request_1()
    except ValueError:
        res1 = "Invalid Card Format"


    # If get checked in 1st request per se
    if not checker.request_1_done:
        tgbot.edit_message(res1)
        return

    # 2nd reqeust
    tgbot.update_status_50()
    res2 = checker.make_request_2()
    tgbot.edit_message(res2)
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


@tgbot.on_message(filters.command("fas"))
def mchk_func(update, message: Message):
    try:
        arg = message.text.split(" ", maxsplit= 1)[1]
        data = [card.strip() for card in arg.split("\n")]
    except Exception:
        TgBot.reply_message("No arguments passed! BSDK", update, message)
        return
    for card in data:
        checker = feedingamerica.Checker(card)
        tgbot = TgBot(update, message)

        result = checker.make_request()
        print(card, result)

        tgbot.edit_message(f"<code>{card}</code>:\n<strong>{result}</strong>")




print("Bot started!")
tgbot.run()

