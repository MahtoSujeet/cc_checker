from pyrogram import Client, filters
import water_1

# Telegram bot initiation
tgbot = Client("bot")

# Checking cmd
@tgbot.on_message(filters.command("chk"))
def chk_func(update, message):
	checker = water_1.Check(update, message)
	#result = checker.run()
	#print(result)


tgbot.run()
