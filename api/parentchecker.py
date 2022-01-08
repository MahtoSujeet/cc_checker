from tg_helper import TgBot
from pyrogram.types import Message


class ParentChecker:
    """init has card as arg"""
    def __init__(self, card: str):
        data = card.split("|")
        self.ccn, self.month, self.year, self.cvv = data[0], data[1], data[2], data[3]


    @staticmethod
    def format_headers(unformatted_headers):
        """Formats Headers"""
        formatted_headers = dict()
        lines = unformatted_headers.split("\n")
        for line in lines:
            if len(line)>1:
              index= line.find(":")
              formatted_headers[line[:index].strip()] = line[index+1:].strip()
        return formatted_headers

