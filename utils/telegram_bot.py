# Telegram bot for sending available banks to telegram channel
import telebot
from core.logger import get_logger

class TelegramBot:
    def __init__(self, token, chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id
        self.logger = get_logger(self.__class__.__name__)

    def send_message(self, message):
        try:
            self.bot.send_message(self.chat_id, message)
            self.logger.debug("Message sent to TELEGRAM.")
        except Exception as e:
            self.logger.error(f"Error in sending msg in telegram: {e}")
