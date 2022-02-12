from pyrogram.types import Message
from pyrogram import Client
import status_message
import re

class TgBot:
    """This class is Telegram Bot connector.

    It will send first message automatically when initiated.
    The message will be status of checking card 0%.

    :param update
    :param message
    """
    def __init__(self, update, message: Message):
        self.update= update
        self.message = message
        self.card = message.text.split(" ", maxsplit= 2)[1].strip()
        self.bot_message = self.send_first_message()


    def send_first_message(self):
        """ Sends first message of 0% progress."""
        msg = self.update.send_message(
            chat_id = self.message.chat.id,
            reply_to_message_id = self.message.message_id,
            text = status_message._0.format(card = self.card),
            parse_mode = "html")
        return msg


    def edit_message(self, text: str):
        """ Edits the message. Arguments: text"""
        self.update.edit_message_text(
            chat_id = self.message.chat.id,
            message_id = self.bot_message.message_id,
            text = text,
            parse_mode = "html"
        )

    def send_video(self, path):
        """ Sends video """
        self.update.send_video(
            chat_id = self.message.chat.id,
            reply_to_message_id = self.message.message_id,
            video = path
        )

    def update_status_50(self):
        """ This updated the status message on telegram to 50%"""
        self.edit_message(
            text = status_message._50.format(card = self.card)
        )


    def update_status_100(self, result, time):
        """Updates(Edits) the telegram message with result"""
        if re.search('card was declined', result) or re.search("card number is incorrect", result) or re.search("invalid", result) or re.search("Invalid", result) or re.search("does not support", result):
            status = "Declined ❌"
        else:
            status = "Approved ✅"

        self.edit_message(
            text = status_message._100.format(
                card = self.card,
                status= status,
                result = result,
                user= self.message.from_user.username,
                time = time
            )
        )

    def send_document(self, path):
        """Sends any file. :param path_to_file"""
        self.update.send_document(
                chat_id= self.message.chat.id,
                reply_to_message_id= self.message.message_id,
                document= path
            )

    @staticmethod
    def reply_message(text: str, update, message: Message):
        update.send_message(
            chat_id= message.chat.id,
            reply_to_message_id= message.message_id,
            text= text,
            parse_mode= "html"
        )
